IMAGE=sklyarov_echo_image
CONTAINER=sklyarov_echo_bot
HUB_IMAGE=olegsklyarov/sklayrov_bot

.PHONY: build run stop push

build:
	docker build -t $(IMAGE) .

run: stop
	docker run --detach \
		--name $(CONTAINER) \
		--env-file .env \
		--restart unless-stopped \
		$(IMAGE)

stop:
	-docker stop $(CONTAINER)
	-docker rm $(CONTAINER)

push: build
	docker tag $(IMAGE) $(HUB_IMAGE):latest
	docker push $(HUB_IMAGE):latest

logs:
	docker logs -f $(CONTAINER)
