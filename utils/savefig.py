import matplotlib.pyplot as plt
import os


def savefig_template(save_flag, base_folder, fig, fn, dpi=100, **kwargs):
    if save_flag:
        fig.savefig(
            os.path.join(base_folder, fn), bbox_inches="tight", dpi=dpi, **kwargs
        )


vars_iv_rename_cols = {
    "demand": "DEMAND",
    "land_avail": "LANDAV",
    "taxable_income": "TAXIN",
    "pv_out": "PVOUT",
    "LV": "LANDVL",
    "SPR": "PENERT",
}
