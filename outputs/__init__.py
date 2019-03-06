import glob, imp, os


def discover_outputs():
    cdir = os.path.dirname(os.path.realpath(__file__))
    output_modules = list(filter(lambda p: not os.path.basename(p).startswith('_'), glob.glob(os.path.join(cdir, '*.py'))))

    return dict([(os.path.basename(os.path.splitext(output_module)[0]), output_module) for output_module in output_modules])


def get_output_by_name(name):
    for om_name, om_path in discover_outputs().items():
        if om_name == name:
            return imp.load_source(om_name, om_path)

    raise LookupError("%s output module not found", name)
