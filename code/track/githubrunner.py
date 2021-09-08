from dotnetcore2 import runtime
runtime._enable_debug_logging()
runtime.ensure_dependencies()
print(runtime._gather_dependencies(runtime._get_bin_folder()))