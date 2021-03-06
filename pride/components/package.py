import os
import importlib
import sys
import types
import inspect
import contextlib
import traceback

import pride.functions.utilities as utilities
import pride.functions.module_utilities as module_utilities

import pride.components.base
import pride.components.fileio
create_module = module_utilities.create_module 
    
def build_documentation_site(module):
    package = Package(module, include_documentation=True)
    utilities.shell("mkdocs build")
    
class Package(pride.components.base.Base):
    
    defaults = {"python_extensions" : (".py", ".pyx", ".pyd", ".pso", ".so"),
                "package_name" : None,
                "include_source" : True,
                "replace_reference_on_load" : False,
                "include_documentation" : False,
                "top_level_package" : '',
                "required_packages" : tuple(),
                "required_modules" : tuple(),
                "ignore_modules" : tuple()}
     
    def _get_subpackages(self):
        return [package for package in self.objects.get("Package", [])]
    subpackages = property(_get_subpackages)
    
    def __init__(self, module, **kwargs):
        self.sources = {}
        documentation = self.documentation = {}
        kwargs.setdefault("package_name", module.__name__)
        super(Package, self).__init__(**kwargs)       
        
        package_name = self.package_name = module.__name__
        top_level_package = self.top_level_package = self.top_level_package or package_name
        include_documentation = self.include_documentation
        include_source = self.include_source
        main_file = getattr(sys.modules["__main__"], "__file__", '__main__')
        module_file = module.__file__
        path, init_py = os.path.split(module_file)
        self.path = path
        
        get_source = module_utilities.get_module_source       
        sources = self.sources      
        try:
            sources[package_name] = get_source(module)        
        except IOError:
            print("No source available for: {}".format(module))
            sources[package_name] = ''
        
        self.required_modules = required_modules = self.required_modules or set()
        self.required_modules = required_packages = self.required_packages or set()
        
        _required_modules, _required_packages = module_utilities.get_required_modules(module)
        required_modules.update(_required_modules)
        required_packages.update(_required_packages)
        
        self.modules = modules = [] # modules that are specifically in this package
        self.packages = [] # Package objects of required package names
        _subpackages = []
        for _file in os.listdir(path):
            module_name, extension = os.path.splitext(_file)
            if module_name in self.ignore_modules or module_name == "__init__":
                continue
            if extension in self.python_extensions:
                modules.append(module_name) # this adds module_name while below adds package.module name, why?
                if module.__package__:
                    module_name = module.__package__ + '.' + module_name

                required_modules.add(module_name)
                with open(os.path.join(path, _file), 'rb') as py_file:
                    source = py_file.read()
                    if include_source:
                        sources[module_name] = source             
                try:
                    _module = (sys.modules.get(module_name) or 
                               module_utilities.create_module(module_name, source,
                                                              context={"__file__" : _file,
                                                                       "_source" : source,
                                                                       "__package__" : package_name}))
                except BaseException as error:
                    if type(error) in (KeyboardInterrupt, SystemExit, RuntimeError):
                        raise
                    print "Unable to compile module: {}. Unable to determine required modules".format(module_name)                 
                    print traceback.format_exc()
                else:
                    _modules, _packages = module_utilities.get_required_modules(_module)
                    required_modules.update(_modules)
                    required_packages.update(_packages)
                    if include_documentation:
                        documentation[module_name] = self.create("pride.components.package.Documentation", 
                                                                 _module, path=path,
                                                                 top_level_package=top_level_package) 
                        
            elif os.path.exists(os.path.join(path, _file, "__init__.py")):
                # do subpackages later so modules in appear grouped by package in mkdocs.yml
                _file = '.'.join((package_name, _file))                
                _module = importlib.import_module(_file)
                _module.__dict__.setdefault("__package__", _file)
                _subpackages.append(_module)                

        package_options = {"sources" : sources,
                           "include_documentation" : include_documentation,
                           "include_source" : include_source,
                           "top_level_package" : top_level_package,
                           "required_packages" : required_packages,
                           "required_modules" : required_modules}
  
        for subpackage in _subpackages:            
            _package = self.create(Package, subpackage, **package_options)            
            required_packages.update(_package.required_packages)
            required_modules.update(_package.required_modules)            
            self.packages.append(_package)

        self.required_packages = required_packages
        required_modules.update(modules)
        self.required_modules = sorted_modules = sorted(required_modules)        
        
        self.relative_imports = dict((_package_name, set()) for _package_name in 
                                      required_packages.union([_p.package_name for _p in self.packages]))
        for _package in required_packages:
            for _module in sorted_modules:
                try:
                    _package_name, __module = _module.split(".", 1)
                except ValueError:
                    continue
                else:
                    if _package == _package_name:
                        self.relative_imports[_package_name].add(__module)
        self.relative_imports[package_name] = set((modules))
        
        if include_source:
            for module_name in required_modules:
                if module_name == "__main__":
                    continue
            #   print "Ensuring source for {} exists".format(module_name)
                if module_name not in sources:
                    try:
                        sources[module_name] = (get_source(sys.modules[module_name] if 
                                                module_name in sys.modules else
                                                get_source(importlib.import_module(module_name))))
                    except:
            #         print "Could not get source for module: ", module_name
                        sources[module_name] = None
        
        if top_level_package == package_name and include_documentation:
            self.documentation[package_name] = self.create("pride.components.package.Documentation", module)  
        
    def find_module(self, module_name, path=None):
        self.alert("{} Looking for module: {}".format(self.package_name, module_name), level=0)
        if module_name in self.required_modules:
            loader = self        
        else:
            loader = None
            for package_name, modules in self.relative_imports.items():
                if module_name in modules:
                    if loader is self:
                        loader = None
                        print "Unable to determine package for relative import", module_name
                        break
                    loader = self
        return loader
        
    def load_module(self, module_name):
        if module_name not in self.sources:
            for package_name, modules in self.relative_imports.items():
                if module_name in modules:
                    module_name = package_name + '.' + module_name
                    break
        try:
            source = self.sources[module_name]
            if not source:
                raise ImportError("Source for module {} not included in package".format(module_name))
        except KeyError:
            raise ImportError
        return module_utilities.create_module(module_name, source)
       
    def __contains__(self, module_name):
        return module_name in self.sources
                                
    def __str__(self):
        return self.reference + ": " + self.package_name
        
        
class Documentation(pride.components.base.Base):
    
    defaults = {"top_level_package" : ''}
    
    def __init__(self, _object, **kwargs):
        super(Documentation, self).__init__(**kwargs)    
        markdown = self.markdown = utilities.documentation(_object)
        module_name = (_object.__module__ if hasattr(_object, "__module__") else
                       _object.__name__).split(".")[-1]
                       
        module = (_object if isinstance(_object, types.ModuleType) else 
                  sys.modules[module_name])
                  
        path, _file = os.path.split(module.__file__)
        
        package_name = (module.__package__ if 
                        module.__package__ is not None else
                        module.__name__.split('.')[0])
        
        package_name = package_name.rsplit(".", 1)[-1]
        md_filepath = os.path.join(path, "docs", package_name, module_name) + ".md" 
        self.md_filepath = md_filepath
        
        yml_entry = r"- ['{}', '{}', '{}']" + "\n"
        entry = yml_entry.format(os.path.join(package_name, module_name) + ".md", 
                                 package_name, module_name)
                                     
        yml_file = os.path.join(path, "mkdocs.yml")
        self.write_markdown_file(markdown, md_filepath)
        self.write_yml_entry(entry, yml_file)
        
    def write_yml_entry(self, entry, yml_file):        
        with open(yml_file, 'a+') as _file:
            contents = _file.read()
            # some sort of windows hijinks can cause IOError errno 0 on files opened for appending
            # this makes it happy and stops it from complaining
            _file.seek(_file.tell()) 
            if entry not in contents:
                if not contents:
                    _file.write("site_name: {}\npages:\n".format(self.top_level_package))
                    _file.write("- ['index.md', 'Homepage']\n")
                _file.write(entry)
                _file.flush()                                                            
        
    def write_markdown_file(self, markdown_text, filename):
        pride.components.fileio.ensure_file_exists(filename, markdown_text)
            
            
if __name__ == "__main__":
    import pride
    package = Package(pride)
    