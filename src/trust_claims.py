from dataclasses import asdict, dataclass
from typing import Any, Dict

from src.errors import EARValidationError


# https://www.ietf.org/archive/id/draft-ietf-rats-ar4si-08.html#section-2.3
@dataclass
class TrustClaim:
    value: int  # must be in range -128 to 127
    tag: str = ""
    short: str = ""
    long: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def validate(self):
        # Validates a TrustClaim object
        if not isinstance(self.value, int) or not -128 <= self.value <= 127:
            raise EARValidationError(
                f"""Invalid value in TrustClaim: {self.value}.
                Must be in range [-128, 127]"""
            )
        if not isinstance(self.tag, str):
            raise EARValidationError("TrustClaim tag must be a string")
        if not isinstance(self.short, str):
            raise EARValidationError("TrustClaim short description must be a string")
        if not isinstance(self.long, str):
            raise EARValidationError("TrustClaim long description must be a string")


# General
VERIFIER_MALFUNCTION_CLAIM = TrustClaim(
    value=-1,
    tag="verifier_malfunction",
    short="verifier malfunction",
    long="A verifier malfunction occurred during the Verifier's appraisal processing.",  # noqa: E501 # pylint: disable=line-too-long
)

NO_CLAIM = TrustClaim(
    value=0,
    tag="no_claim",
    short="no claim being made",
    long="The Evidence received is insufficient to make a conclusion.",
)

UNEXPECTED_EVIDENCE_CLAIM = TrustClaim(
    value=1,
    tag="unexected_evidence",
    short="unexpected evidence",
    long="The Evidence received contains unexpected elements which the Verifier is unable to parse.",  # noqa: E501 # pylint: disable=line-too-long
)

CRYPTO_VALIDATION_FAILED_CLAIM = TrustClaim(
    value=99,
    tag="crypto_failed",
    short="cryptographic validation failed",
    long="Cryptographic validation of the Evidence has failed.",
)


# Instance Identity
TRUSTWORTHY_INSTANCE_CLAIM = TrustClaim(
    value=2,
    tag="recognized_instance",
    short="recognized and not compromised",
    long="The Attesting Environment is recognized, and the associated instance of the Attester is not known to be compromised.",  # noqa: E501 # pylint: disable=line-too-long
)

UNTRUSTWORTHY_INSTANCE_CLAIM = TrustClaim(
    value=96,
    tag="untrustworthy_instance",
    short="recognized but not trustworthy",
    long="The Attesting Environment is recognized, but its unique private key indicates a device which is not trustworthy.",  # noqa: E501 # pylint: disable=line-too-long
)

UNRECOGNIZED_INSTANCE_CLAIM = TrustClaim(
    value=97,
    tag="unrecognized_instance",
    short="not recognized",
    long="The Attesting Environment is not recognized; however the Verifier believes it should be.",  # noqa: E501 # pylint: disable=line-too-long
)


# Config
APPROVED_CONFIG_CLAIM = TrustClaim(
    value=2,
    tag="approved_config",
    short="all recognized and approved",
    long="The configuration is a known and approved config.",
)

NO_CONFIG_VULNS_CLAIM = TrustClaim(
    value=3,
    tag="safe_config",
    short="no known vulnerabilities",
    long="The configuration includes or exposes no known vulnerabilities",  # noqa: E501 # pylint: disable=line-too-long
)

UNSAFE_CONFIG_CLAIM = TrustClaim(
    value=32,
    tag="unsafe_config",
    short="known vulnerabilities",
    long="The configuration includes or exposes known vulnerabilities.",
)

UNSUPPORTABLE_CONFIG_CLAIM = TrustClaim(
    value=96,
    tag="unsupportable_config",
    short="unacceptable security vulnerabilities",
    long="The configuration is unsupportable as it exposes unacceptable security vulnerabilities",  # noqa: E501 # pylint: disable=line-too-long
)


# Executables & Runtime
APPROVED_RUNTIME_CLAIM = TrustClaim(
    value=2,
    tag="approved_rt",
    short="recognized and approved boot- and run-time",
    long="Only a recognized genuine set of approved executables, scripts, files, and/or objects have been loaded during and after the boot process.",  # noqa: E501 # pylint: disable=line-too-long
)

APPROVED_BOOT_CLAIM = TrustClaim(
    value=3,
    tag="approved_boot",
    short="recognized and approved boot-time",
    long="Only a recognized genuine set of approved executables have been loaded during the boot process.",  # noqa: E501 # pylint: disable=line-too-long
)

UNSAFE_RUNTIME_CLAIM = TrustClaim(
    value=32,
    tag="unsafe_rt",
    short="recognized but known bugs or vulnerabilities",
    long="Only a recognized genuine set of executables, scripts, files, and/or objects have been loaded. However the Verifier cannot vouch for a subset of these due to known bugs or other known vulnerabilities.",  # noqa: E501 # pylint: disable=line-too-long
)

UNRECOGNIZED_RUNTIME_CLAIM = TrustClaim(
    value=33,
    tag="unrecognized_rt",
    short="unrecognized run-time",
    long="Runtime memory includes executables, scripts, files, and/or objects which are not recognized.",  # noqa: E501 # pylint: disable=line-too-long
)

CONTRAINDICATED_RUNTIME_CLAIM = TrustClaim(
    value=96,
    tag="contraindicated_rt",
    short="contraindicated run-time",
    long="Runtime memory includes executables, scripts, files, and/or object which are contraindicated.",  # noqa: E501 # pylint: disable=line-too-long
)


# File System
APPROVED_FILES_CLAIM = TrustClaim(
    value=2,
    tag="approved_fs",
    short="all recognized and approved",
    long="Only a recognized set of approved files are found.",
)

UNRECOGNIZED_FILES_CLAIM = TrustClaim(
    value=32,
    tag="unrecognized_fs",
    short="unrecognized item(s) found",
    long="The file system includes unrecognized executables, scripts, or files.",  # noqa: E501 # pylint: disable=line-too-long
)

CONTRAINDICATED_FILES_CLAIM = TrustClaim(
    value=96,
    tag="contraindicated_fs",
    short="contraindicated item(s) found",
    long="The file system includes contraindicated executables, scripts, or files.",  # noqa: E501 # pylint: disable=line-too-long
)


# Hardware
GENUINE_HARDWARE_CLAIM = TrustClaim(
    value=2,
    tag="genuine_hw",
    short="genuine",
    long="An Attester has passed its hardware and/or firmware verifications needed to demonstrate that these are genuine/supported.",  # noqa: E501 # pylint: disable=line-too-long
)

UNSAFE_HARDWARE_CLAIM = TrustClaim(
    value=32,
    tag="unsafe_hw",
    short="genuine but known bugs or vulnerabilities",
    long="An Attester contains only genuine/supported hardware and/or firmware, but there are known security vulnerabilities.",  # noqa: E501 # pylint: disable=line-too-long
)

CONTRAINDICATED_HARDWARE_CLAIM = TrustClaim(
    value=96,
    tag="contraindicated_hw",
    short="genuine but contraindicated",
    long="Attester hardware and/or firmware is recognized, but its trustworthiness is contraindicated.",  # noqa: E501 # pylint: disable=line-too-long
)

UNRECOGNIZED_HARDWARE_CLAIM = TrustClaim(
    value=97,
    tag="unrecognized_hw",
    short="unrecognized",
    long="A Verifier does not recognize an Attester's hardware or firmware, but it should be recognized.",  # noqa: E501 # pylint: disable=line-too-long
)


# Opaque Runtime
ENCRYPTED_MEMORY_RUNTIME_CLAIM = TrustClaim(
    value=2,
    tag="encrypted_rt",
    short="memory encryption",
    long="the Attester's executing Target Environment and Attesting Environments are encrypted and within Trusted Execution Environment(s) opaque to the operating system, virtual machine manager, and peer applications.",  # noqa: E501 # pylint: disable=line-too-long
)

ISOLATED_MEMORY_RUNTIME_CLAIM = TrustClaim(
    value=32,
    tag="isolated_rt",
    short="memory isolation",
    long="the Attester's executing Target Environment and Attesting Environments are inaccessible from any other parallel application or Guest VM running on the Attester's physical device.",  # noqa: E501 # pylint: disable=line-too-long
)

VISIBLE_MEMORY_RUNTIME_CLAIM = TrustClaim(
    value=96,
    tag="visible_rt",
    short="visible",
    long="The Verifier has concluded that in memory objects are unacceptably visible within the physical host that supports the Attester.",  # noqa: E501 # pylint: disable=line-too-long
)


# Opaque Storage
HW_KEYS_ENCRYPTED_SECRETS_CLAIM = TrustClaim(
    value=2,
    tag="hw_encrypted_secrets",
    short="encrypted secrets with HW-backed keys",
    long="the Attester encrypts all secrets in persistent storage via using keys which are never visible outside an HSM or the Trusted Execution Environment hardware.",  # noqa: E501 # pylint: disable=line-too-long
)

SW_KEYS_ENCRYPTED_SECRETS_CLAIM = TrustClaim(
    value=32,
    tag="sw_encrypted_secrets",
    short="encrypted secrets with non HW-backed keys",
    long="the Attester encrypts all persistently stored secrets, but without using hardware backed keys.",  # noqa: E501 # pylint: disable=line-too-long
)

UNENCRYPTED_SECRETS_CLAIM = TrustClaim(
    value=96,
    tag="unencrypted_secrets",
    short="unencrypted secrets",
    long="There are persistent secrets which are stored unencrypted in an Attester.",
)


# Sourced Data
TRUSTED_SOURCES_CLAIM = TrustClaim(
    value=2,
    tag="trusted_sources",
    short="from attesters in the affirming tier",
    long='All essential Attester source data objects have been provided by other Attester(s) whose most recent appraisal(s) had both no Trustworthiness Claims of "0" where the current Trustworthiness Claim is "Affirming", as well as no "Warning" or "Contraindicated" Trustworthiness Claims.',  # noqa: E501 # pylint: disable=line-too-long
)

UNTRUSTED_SOURCES_CLAIM = TrustClaim(
    value=32,
    tag="untrusted_sources",
    short="from unattested sources or attesters in the warning tier",
    long='Attester source data objects come from unattested sources, or attested sources with "Warning" type Trustworthiness Claims',  # noqa: E501 # pylint: disable=line-too-long
)

CONTRAINDICATED_SOURCES_CLAIM = TrustClaim(
    value=96,
    tag="contraindicated_sources",
    short="from attesters in the contraindicated tier",
    long="Attester source data objects come from contraindicated sources.",
)
