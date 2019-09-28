from channels.routing import ProtocolTypeRouter  # type: ignore

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
})  # pylint: disable=invalid-name
