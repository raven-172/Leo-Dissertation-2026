#from ultralytics.nn.modules import CustomBlock 
from block_add import *

def parse_model(d, ch, verbose=True):
    """Parse a YOLO model.yaml dictionary into a PyTorch model."""
    import ast

    legacy = True
    max_channels = float("inf")
    nc, act, scales, end2end = (d.get(x) for x in ("nc", "activation", "scales", "end2end"))
    reg_max = d.get("reg_max", 16)
    depth, width, kpt_shape = (d.get(x, 1.0) for x in ("depth_multiple", "width_multiple", "kpt_shape"))
    scale = d.get("scale")
    if scales:
        if not scale:
            scale = next(iter(scales.keys()))
            LOGGER.warning(f"no model scale passed. Assuming scale='{scale}'.")
        depth, width, max_channels = scales[scale]
    restricted = _SafeLoad.restricted()
    if act:
        Conv.default_act = _SafeLoad.activation(act) if restricted else eval(act)
        if verbose:
            LOGGER.info(f"{colorstr('activation:')} {act}")
    if verbose:
        LOGGER.info(f"\n{'':>3}{'from':>20}{'n':>3}{'params':>10}  {'module':<45}{'arguments':<30}")

    ch = [ch]
    layers, save, c2 = [], [], ch[-1]
    base_modules = frozenset(
        {
            Classify,
            Conv,
            ConvTranspose,
            GhostConv,
            Bottleneck,
            GhostBottleneck,
            SPP,
            SPPF,
            C2fPSA,
            C2PSA,
            DWConv,
            Focus,
            BottleneckCSP,
            C1,
            C2,
            C2f,
            C3k2,
            RCAC3k,
            RCAC3k2,
            RepNCSPELAN4,
            ELAN1,
            ADown,
            AConv,
            SPPELAN,
            C2fAttn,
            C3,
            C3TR,
            C3Ghost,
            torch.nn.ConvTranspose2d,
            DWConvTranspose2d,
            C3x,
            RepC3,
            PSA,
            SCDown,
            C2fCIB,
            A2C2f,
        }
    )
    repeat_modules = frozenset(
        {
            BottleneckCSP,
            C1,
            C2,
            C2f,
            C3k2,
            RCAC3k,
            RCAC3k2,
            C2fAttn,
            C3,
            C3TR,
            C3Ghost,
            C3x,
            RepC3,
            C2fPSA,
            C2fCIB,
            C2PSA,
            A2C2f,
        }
    )

    for i, (f, n, m, args) in enumerate(d["backbone"] + d["head"]):
        m = (
            getattr(torch.nn, m[3:])
            if m.startswith("nn.")
            else getattr(__import__("torchvision").ops, m[16:])
            if m.startswith("torchvision.ops.")
            else globals()[m]
        )
        if restricted and not (isinstance(m, type) and issubclass(m, torch.nn.Module)):
            raise TypeError(emojis(f"ERROR ❌️ module '{m}' is not a permitted model layer under restricted loading."))
        for j, a in enumerate(args):
            if isinstance(a, str):
                with contextlib.suppress(ValueError):
                    args[j] = locals()[a] if a in locals() else ast.literal_eval(a)

        n = n_ = max(round(n * depth), 1) if n > 1 else n
        if m in base_modules:
            c1, c2 = ch[f], args[0]
            if m is not Classify:
                c2 = make_divisible(min(c2, max_channels) * width, 8)
            if m is C2fAttn:
                args[2] = int(max(round(min(args[2], max_channels // 2 // 32)) * width, 1) if args[2] > 1 else args[2])
                hidden_channels = int(c2 * (args[6] if len(args) > 6 else 0.5))
                if hidden_channels % args[2]:
                    raise ValueError(
                        f"C2fAttn hidden channels {hidden_channels} (from c2={c2}) must be divisible by nh={args[2]}; "
                        "adjust width_multiple, nh, or C2fAttn expansion"
                    )
                args[1] = hidden_channels
            args = [c1, c2, *args[1:]]
            if m in repeat_modules:
                args.insert(2, n)
                n = 1
            if m in {C3k2, RCAC3k2}:
                legacy = False
                if scale in "mlx":
                    args[3] = True
            if m is A2C2f:
                legacy = False
                if scale in "lx":
                    args.extend((True, 1.2))
            if m is C2fCIB:
                legacy = False
        elif m is AIFI:
            args = [ch[f], *args]
        elif m in frozenset({HGStem, HGBlock}):
            c1, cm, c2 = ch[f], args[0], args[1]
            args = [c1, cm, c2, *args[2:]]
            if m is HGBlock:
                args.insert(4, n)
                n = 1
        elif m is ResNetLayer:
            c2 = args[1] if args[3] else args[1] * 4
        elif m is torch.nn.BatchNorm2d:
            args = [ch[f]]
        elif m is Concat:
            c2 = sum(ch[x] for x in f)
        elif m in frozenset(
            {
                Detect,
                WorldDetect,
                YOLOEDetect,
                Segment,
                Segment26,
                YOLOESegment,
                YOLOESegment26,
                Pose,
                Pose26,
                OBB,
                OBB26,
            }
        ):
            args.extend([reg_max, end2end, [ch[x] for x in f]])
            if m in {Segment, YOLOESegment, Segment26, YOLOESegment26}:
                args[2] = make_divisible(min(args[2], max_channels) * width, 8)
            if m in {Detect, YOLOEDetect, Segment, Segment26, YOLOESegment, YOLOESegment26, Pose, Pose26, OBB, OBB26}:
                m.legacy = legacy
        elif m is Depth:
            args = [*args[:1], [ch[x] for x in f]]
        elif m is SemanticSegment:
            args.append([ch[x] for x in f])
        elif m is v10Detect:
            args.append([ch[x] for x in f])
        elif m is ImagePoolingAttn:
            args.insert(1, [ch[x] for x in f])
        elif m is RTDETRDecoder:
            args.insert(1, [ch[x] for x in f])
        elif m is CBLinear:
            c2 = args[0]
            c1 = ch[f]
            args = [c1, c2, *args[1:]]
        elif m is CBFuse:
            c2 = ch[f[-1]]
        elif m in frozenset({TorchVision, Index}):
            c2 = args[0]
            c1 = ch[f]
            args = [*args[1:]]
        elif m in frozenset({CA, RCAB, RCAC3k, RCAC3k2}):
            c1 = ch[f]
            c2 = c1
            args = [c1, *args]
        else:
            c2 = ch[f]

        m_ = torch.nn.Sequential(*(m(*args) for _ in range(n))) if n > 1 else m(*args)
        t = str(m)[8:-2].replace("__main__.", "")
        m_.np = sum(x.numel() for x in m_.parameters())
        m_.i, m_.f, m_.type = i, f, t
        if verbose:
            LOGGER.info(f"{i:>3}{f!s:>20}{n_:>3}{m_.np:10.0f}  {t:<45}{args!s:<30}")
        save.extend(x % i for x in ([f] if isinstance(f, int) else f) if x != -1)
        layers.append(m_)
        if i == 0:
            ch = []
        ch.append(c2)

    return torch.nn.Sequential(*layers), sorted(save)
