IMAGE=sklyarov_echo_image
CONTAINER=sklyarov_echo_bot
GHCR_IMAGE=ghcr.io/olegsklyarov/sklyarov_echo_image

.PHONY: build run stop publish

build:
	docker build -t $(IMAGE) .

run:
	docker run -d --name $(CONTAINER) --env-file .env $(IMAGE)

stop:
	docker stop $(CONTAINER) && docker rm $(CONTAINER)

publish: build
	docker tag $(IMAGE) $(GHCR_IMAGE):latest
	docker push $(GHCR_IMAGE):latest
