"""One bounded installed-runtime observation; no DET caller or science imports."""
import sys
import os
import json
import hashlib
import _hashlib
import decimal
import fractions
import site
import _pydecimal


def profile():
    return {
        'version': sys.version, 'implementation': sys.implementation.name,
        'version_info': list(sys.version_info), 'executable': sys.executable,
        'prefix': sys.prefix, 'base_prefix': sys.base_prefix,
        'exec_prefix': sys.exec_prefix, 'base_exec_prefix': sys.base_exec_prefix,
        'path': list(sys.path), 'byteorder': sys.byteorder,
        'isolated': sys.flags.isolated,
        'dont_write_bytecode': sys.flags.dont_write_bytecode,
        'optimize': sys.flags.optimize,
    }


before = profile()
decimal_extension_error = None
try:
    import _decimal
except ImportError as error:
    decimal_extension_error = {'type': type(error).__name__, 'message': str(error)}

hash_observations = {
    'sha256_empty': hashlib.sha256(b'').hexdigest(),
    'openssl_sha256_empty': _hashlib.new('sha256', b'').hexdigest(),
    'available_openssl_names': sorted(_hashlib.openssl_md_meth_names),
}

modules = {}
for name, module in sorted(sys.modules.items()):
    if module is None:
        continue
    spec = getattr(module, '__spec__', None)
    modules[name] = {
        'file': getattr(module, '__file__', None),
        'cached': getattr(module, '__cached__', None),
        'origin': getattr(spec, 'origin', None),
        'loader_type': type(getattr(spec, 'loader', None)).__name__,
    }

value = {
    'schema': 'ri121-installed-runtime-profile-observation-v1',
    'profile_before': before, 'profile_after': profile(),
    'uname': list(os.uname()),
    'startup': {
        'enable_user_site': site.ENABLE_USER_SITE,
        'site_prefixes': site.PREFIXES,
        'distutils_hook_loaded': '_distutils_hack' in sys.modules,
        'sitecustomize_loaded': 'sitecustomize' in sys.modules,
        'usercustomize_loaded': 'usercustomize' in sys.modules,
    },
    'decimal': {
        'extension_loaded': '_decimal' in sys.modules,
        'fallback_loaded': '_pydecimal' in sys.modules,
        'decimal_class_is_fallback': decimal.Decimal is _pydecimal.Decimal,
        'extension_import_error': decimal_extension_error,
        'fraction_class_module': fractions.Fraction.__module__,
    },
    'hashlib': hash_observations,
    'modules': modules,
    'scientific_targets_imported_or_executed': False,
    'boundary': 'Installed-runtime observation under pinned supplier, cache-selection and host premises; no scientific qualification.',
}
sys.stdout.write(json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + '\n')
