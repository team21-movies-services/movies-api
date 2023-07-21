create_network:
	@docker network create movies-network 2>/dev/null || echo "movies-network is up-to-date"

# DEVELOPMENT
.PHONY: up-local
up-local: create_network
	@docker-compose -f docker-compose.local.yaml up --build

.PHONY: build-local
build-local:
	@docker-compose -f docker-compose.local.yaml build --force-rm

.PHONY: down-local
down-local:
	@docker-compose -f docker-compose.local.yaml down

.PHONY: uninstall-local
uninstall-local:
	@docker-compose -f docker-compose.local.yaml down --remove-orphans --volumes


# TESTS
.PHONY: up-tests
up-tests:
	@docker-compose -f docker-compose.tests.yaml up --build

.PHONY: uninstall-tests
uninstall-tests:
	@docker-compose -f docker-compose.tests.yaml down --remove-orphans --volumes
