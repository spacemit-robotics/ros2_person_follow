from .core import CvBridge, CvBridgeError

__all__ = ["CvBridge", "CvBridgeError"]

# python bindings
try:
    # This try is just to satisfy doc jobs that are built differently.
    from .boost.cv_bridge_boost import cvtColorForDisplay, getCvType
    __all__ += ["cvtColorForDisplay", "getCvType"]
except ImportError:
    pass
