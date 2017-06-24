# tl;dr

```
make build
make run
```

The running container will be running both, a beeping binary and the python script prometheus exporter.

# beeping_exporter

The [beeping service](https://github.com/yanc0/beeping) is a great tool for monitoring web sites. Adding a prometheus exporter allows for integration into a monitoring stack where alerts can be defined and historical data can be accesible.

# container image

The [phusion baseimage](https://hub.docker.com/r/phusion/baseimage/) image provides an easy way to declare and manage running services inside the container. For simplicity purposes,



# configuration

Configuration is setup via environment variables declared in the `beeping_exporter.env` file.

A helper script is provided for maintaining configuration in a yaml file: `files/beeping.yaml`.

```
CONFIG_JSON=$(files/yaml2json.py < files/beeping.yaml)
cp files/beeping_exporter.env.tpl beeping_exporter.env
echo "BEEPING_CHECKS=$CONFIG_JSON" >> beeping_exporter.env
```

# TODO

* Add graphite exporting using prometheus library support.
* Use docker multi-stage build to compile latest beeping binary and add it to the image.


