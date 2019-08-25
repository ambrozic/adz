## ADZ
[![](https://img.shields.io/pypi/pyversions/adz.svg)](https://pypi.python.org/pypi/adz)
[![](https://img.shields.io/pypi/v/adz.svg)](https://pypi.python.org/pypi/adz)
[![](https://img.shields.io/pypi/wheel/adz.svg)](https://pypi.python.org/pypi/adz)
[![](https://travis-ci.org/ambrozic/adz.svg?branch=master)](https://travis-ci.org/ambrozic/adz)
[![](https://codecov.io/github/ambrozic/adz/coverage.svg?branch=master)](https://codecov.io/github/ambrozic/adz)
[![](https://img.shields.io/pypi/l/adz.svg)](https://pypi.python.org/pypi/adz)

Command line interface for HTTP requests defined in yaml configuration file.

### Install
`pip install adz`

### Quick start
Having a yaml configuration file

```
endpoints:
  endpoint:
    request: GET https://httpbin.org/get
    headers:
      Content-Type: application/json
```

and running on command line

`adz endpoint`

will execute `endpoint` request defined in configuration file and print

```
GET https://httpbin.org/get
HTTP/1.1 200 OK
 • access-control-allow-credentials: true
 • access-control-allow-origin: *
 • content-encoding: gzip
 • content-type: application/json
 • date: Thu, 06 Jun 2019 06:06:06 GMT
 • referrer-policy: no-referrer-when-downgrade
 • server: nginx
 • x-content-type-options: nosniff
 • x-frame-options: DENY
 • x-xss-protection: 1; mode=block
 • content-length: 204
 • connection: keep-alive

{
    "args": {},
    "headers": {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/json",
        "Host": "httpbin.org",
        "User-Agent": "python-httpx/0.7.1"
    },
    "url": "https://httpbin.org/get"
}
```


### Configuration
For an example configuration look at [docs/example.yml](https://github.com/ambrozic/adz/blob/master/docs/example.yml).

#### settings
- colors: `bool`, default: `true`
    - control output print in colors 
- response: `bool`, default: `true`
    - control response body output
- theme: `str`, default `native`
    - any theme name from [here](https://help.farbox.com/pygments.html) should work

#### variables
- used to interpolate values in headers and urls
    - `variable: abc` applied on `url: http://example.org/$variable` results in `http://example.org/abc`
- variable value starting with `file://` is opened as file and loaded as string into variable

#### endpoints
- description
- method
    - http methods
- url
- request
    - `method url` e.g. `get http://example.org`
- params
    - query string parameters
- headers
- json 
    - json string
    - string starting with `file://` is loaded as json file  
- data
    - json string
    - string starting with `file://` is loaded as json file
- cookies
- files
    - path to a file: `path/to/file.txt`
    - file name and path: `filename: path/to/file.txt`


#### Configuration file 

##### Expected configuration file names

- `adz.yaml` or `adz.yml`
- `api.yaml` or `api.yml`
- `rest.yaml` or `rest.yml`

##### Expected locations

- current location: `.`
- user's home: `~/` 
- `.adz` directory in user's home e.g. `~/.adz/` 

Configuration file path can also be set using environmental variable `ADZ`.


### CLI
Run `adz -h`

#### commands
- `adz --config`, `adz -c`
    - path to yaml configuration file
    
- `adz --details <endpoint>`, `adz -d <endpoint>`
    - output details about endpoint from configuration file
    
- `adz --list`, `adz -l`
    - list available endpoints in configuration file
    
- `adz --output`, `adz -o`
    - output processed configuration file as json

- `adz --settings`, `adz -s`
    - output settings in configuration file    

- `adz --var name=value`, `adz -v name=value`
    - set or override variables in configuration

- `adz --colors`, `adz --no-colors`
    - control output print in colors
    
- `adz --response`, `adz --no-response`
    - control response body output
    

### License

ADZ is licensed under a three clause BSD License. Full license text can be found [here](https://github.com/ambrozic/adz/blob/master/license).
