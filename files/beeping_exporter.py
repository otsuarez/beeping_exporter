#!/usr/bin/env python

import re
import time
import requests
import argparse
from pprint import pprint
import ast

import os
from sys import exit
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

DEBUG = int(os.environ.get('DEBUG', '0'))

def must_env(var):
    val = os.environ.get(var)
    if val is None:
        raise Exception('Error reading token from environment (%s)' % var)

    return val

def load_env():
    global BEEPING_SERVER
    global BEEPING_METRICS_PORT
    global BEEPING_CHECKS

    BEEPING_SERVER = must_env('BEEPING_SERVER')
    BEEPING_METRICS_PORT = must_env('BEEPING_METRICS_PORT')
    BEEPING_CHECKS = must_env('BEEPING_CHECKS')

    
class BeepingCollector(object):
    # The sites we want to monitor.
    sites = ast.literal_eval(must_env('BEEPING_CHECKS'))

    def __init__(self, target):
        self._target = target.rstrip("/")

    def collect(self):
        sites_data = self._request_data()

        self._setup_empty_prometheus_metrics()

        for site in self.sites:
            if DEBUG:
                print "working with site: %s" % site
                pprint(sites_data[site])
            self._get_metrics(site,sites_data[site])

        if DEBUG:
            print "_prometheus_metrics" 
            pprint(self._prometheus_metrics)
        for metric in self._prometheus_metrics.values():
            yield metric

    def _request_data(self):
        # Request the information we need from Beeping
        beeping_url = '{0}/check'.format(self._target) # @TODO no need for the format i think 
        if DEBUG:
            print "_request_data >> beeping_url: %s" % beeping_url

        def queryBeeping(myurl):
            result = {}
            for site in self.sites:
                result[site] = {}
                data = {}
                params = self.sites[site]
                response = requests.post(myurl, json=params)
                if response.status_code != requests.codes.ok:
                    return[]
                data = response.json()
                result[site] = data
            return result

        return queryBeeping(beeping_url)

    def _setup_empty_prometheus_metrics(self):
        # The metrics we want to export.
        self._prometheus_metrics = {}
        self._prometheus_metrics = {
            'dns_lookup':
                GaugeMetricFamily('beeping_dns_lookup',
                                  'site dns_lookup in seconds', labels=["site"]),
            'tcp_connection':
                GaugeMetricFamily('beeping_tcp_connection',
                                  'site tcp_connection in seconds', labels=["site"]),
            'tls_handshake':
                GaugeMetricFamily('beeping_tls_handshake',
                                  'site tls_handshake in seconds', labels=["site"]),
            'server_processing':
                GaugeMetricFamily('beeping_server_processing',
                                  'site server_processing in seconds', labels=["site"]),
            'content_transfer':
                GaugeMetricFamily('beeping_content_transfer',
                                  'site content_transfer in seconds', labels=["site"]),
            'http_request_time':
                GaugeMetricFamily('beeping_http_request_time_seconds',
                                  'site http_request_time in seconds', labels=["site"]),
            'http_status_code':
                GaugeMetricFamily('beeping_http_status_code',
                                  'site http_status_code', labels=["site"]),
            'http_body_pattern':
                GaugeMetricFamily('beeping_http_body_pattern',
                                  'site http_body_pattern found', labels=["site"]),
            'timeline_name_lookup':
                GaugeMetricFamily('beeping_timeline_name_lookup',
                                  'site timeline name_lookup in seconds', labels=["site"]),
            'timeline_connect':
                GaugeMetricFamily('beeping_timeline_connect',
                                  'site timeline connect in seconds', labels=["site"]),
            'timeline_pretransfer':
                GaugeMetricFamily('beeping_timeline_pretransfer',
                                  'site timeline pretransfer in seconds', labels=["site"]),
            'timeline_starttransfer':
                GaugeMetricFamily('beeping_timeline_starttransfer',
                                  'site timeline starttransfer in seconds', labels=["site"]),
            'ssl_cert_expiry_days_left':
                GaugeMetricFamily('beeping_ssl_cert_expiry_days_left',
                                  'ssl cert expiry days left', labels=["site"]),
        }

    def _get_metrics(self, site, site_data):
        if DEBUG:
            print "====== get_metrics checking site: "+site 
            print site_data.get('http_status_code')
        if site_data.get('http_status_code', 0):
            self._prometheus_metrics['http_status_code'].add_metric([site], site_data.get('http_status_code'))
        if site_data.get('http_body_pattern'): 
            http_body_pattern_value = 1
        else:
            http_body_pattern_value = 0
        self._prometheus_metrics['http_body_pattern'].add_metric([site], http_body_pattern_value)
        # metrics
        self._prometheus_metrics['dns_lookup'].add_metric([site], site_data.get('dns_lookup'))
        self._prometheus_metrics['tcp_connection'].add_metric([site], site_data.get('tcp_connection'))
        if site_data.get('tls_handshake', 0):
            self._prometheus_metrics['tls_handshake'].add_metric([site], site_data.get('tls_handshake'))
        self._prometheus_metrics['server_processing'].add_metric([site], site_data.get('server_processing'))
        self._prometheus_metrics['content_transfer'].add_metric([site], site_data.get('content_transfer'))
        self._prometheus_metrics['http_request_time'].add_metric([site], site_data.get('http_request_time'))
        # timeline data
        self._prometheus_metrics['timeline_name_lookup'].add_metric([site], site_data.get('timeline',0).get('name_lookup',0))
        self._prometheus_metrics['timeline_connect'].add_metric([site], site_data.get('timeline',0).get('connect',0))
        self._prometheus_metrics['timeline_pretransfer'].add_metric([site], site_data.get('timeline',0).get('pretransfer',0))
        self._prometheus_metrics['timeline_starttransfer'].add_metric([site], site_data.get('timeline',0).get('starttransfer',0))
        # ssl 
        if site_data.get('ssl'):
            self._prometheus_metrics['ssl_cert_expiry_days_left'].add_metric([site], site_data.get('ssl').get('cert_expiry_days_left'))
            

def parse_args():
    parser = argparse.ArgumentParser(
        description='beeping exporter args beeping address and port'
    )
    parser.add_argument(
        '-j', '--beeping',
        metavar='beeping',
        required=False,
        help='server url from the beeping api',
        default=os.environ.get('BEEPING_SERVER', 'http://localhost:8080')
    )
    parser.add_argument(
        '-p', '--port',
        metavar='port',
        required=False,
        type=int,
        help='Listen to this port',
        default=int(os.environ.get('BEEPING_METRICS_PORT', '9118'))
    )
    return parser.parse_args()


BEEPING_SERVER = None
BEEPING_METRICS_PORT = None
BEEPING_CHECKS = None

def main():
    try:
        load_env()
        args = parse_args()
        port = int(args.port)
        REGISTRY.register(BeepingCollector(args.beeping))
        start_http_server(port)
        print "Polling %s. Serving at port: %s" % (args.beeping, port)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(" Interrupted")
        exit(0)


if __name__ == "__main__":
    main()

