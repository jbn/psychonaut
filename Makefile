.PHONY: refresh_canonical_lexicons
refresh_canonical_lexicons:
	@echo "Refreshing canonical lexicons..."

	@echo "  - Fetching latest canonical lexicons..." && \
		temp_dir=$$(mktemp -d) && \
		git clone git@github.com:bluesky-social/atproto.git "$$temp_dir" && \
	echo "  - Removing old canonical lexicons..." && \
		rm -rf lexicons && \
	echo "  - Copying new canonical lexicons..." && \
		mv "$$temp_dir/lexicons" . && \
	echo "  - Cleaning up..." && \
		rm -rf "$$temp_dir";
