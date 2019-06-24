from ykman.util import is_cve201715361_vulnerable_firmware_version
from .util import _get_test_method_names


def yubikey_condition(condition):
    def decorate_method(method):
        method_conditions = (
            getattr(method, '_yubikey_conditions')
            if '_yubikey_conditions' in dir(method)
            else set())
        method_conditions.add(condition)
        setattr(method, '_yubikey_conditions', method_conditions)
        return method

    def decorate_class(cls):
        for method_name in _get_test_method_names(cls):
            setattr(
                cls,
                method_name,
                decorate_method(getattr(cls, method_name)))
        return cls

    def decorate(method_or_class):
        if type(method_or_class) is type:
            return decorate_class(method_or_class)
        else:
            return decorate_method(method_or_class)

    return decorate


@yubikey_condition
def is_fips(dev):
    return dev.is_fips


@yubikey_condition
def is_not_fips(dev):
    return not dev.is_fips


@yubikey_condition
def is_neo(dev):
    return dev.version < (4, 0, 0)


@yubikey_condition
def is_not_neo(dev):
    return dev.version >= (4, 0, 0)


@yubikey_condition
def supports_piv_attestation(dev):
    return dev.version >= (4, 3, 0)


@yubikey_condition
def not_supports_piv_attestation(dev):
    return dev.version < (4, 3, 0)


@yubikey_condition
def is_roca(dev):
    return is_cve201715361_vulnerable_firmware_version(dev.version)


@yubikey_condition
def is_not_roca(dev):
    return not is_cve201715361_vulnerable_firmware_version(dev.version)


@yubikey_condition
def can_write_config(dev):
    return dev.can_write_config


def version_min(min_version):
    return yubikey_condition(lambda dev: dev.version >= min_version)


def version_in_range(min_inclusive, max_inclusive):
    return yubikey_condition(
        lambda dev:
        min_inclusive <= dev.version <= max_inclusive
    )


def version_not_in_range(min_inclusive, max_inclusive):
    return yubikey_condition(
        lambda dev:
        dev.version < min_inclusive or dev.version > max_inclusive
    )
