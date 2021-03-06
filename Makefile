include util.mk


# =============
# Configuration
# =============

$(eval imagecast  := $(venv)/bin/imagecast)


# =====
# Setup
# =====

# Install requirements for development.
setup-package: virtualenv-dev
	@test -e $(imagecast) || $(pip) install --upgrade --editable=.[service]
