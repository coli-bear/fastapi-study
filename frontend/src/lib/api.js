import qs from "qs"

function _generate_url(method, url, params) {
    let _url = `${import.meta.env.VITE_SERVER_URL}${url.startsWith('/') ? url : '/' + url}`;
    if (method.toLowerCase() === 'get' && params && Object.keys(params).length > 0) {
        const queryString = new URLSearchParams(params).toString();
        _url += '?' + queryString;
    }
    return _url;
}

const _is_error = (response) => {
    if (!!response) {
        return !(response.status >= 200 && response.status < 300);
    }

    return true;
}

function _failure_callback(json, failure_callback) {
    if (failure_callback) {
        failure_callback(json)

    } else {
        alert(JSON.stringify(json))
    }
}

function _success_callback(json, success_callback) {
    if (!success_callback) {
        return
    }
    if (json) {
        success_callback(json)
    } else {
        success_callback()
    }
}

function default_options(method, params, content_type = 'application/json') {
    let options = {
        method: method,
        headers: {
            'Content-Type': content_type,
            'Accept': content_type
        }
    }
    if (method !== 'get') {
        options['body'] = JSON.stringify(params);
    }
    return options
}

function signin_options(params) {
    return {
        method: 'post',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        },
        body: qs.stringify(params)
    }
}

export const fastapi = (operation, url, params, success_callback, failure_callback) => {
    let method = operation.toLowerCase();
    let _url = _generate_url(method, url, params);
    let options = method === 'signin' ? signin_options(params) : default_options(method, params)


    fetch(_url, options)
        .then((response) => {
            if (response.status === 201) {
                _success_callback(undefined, success_callback)
            }

            response
                .json()
                .then((json) => {
                    if (_is_error(response)) {
                        _failure_callback(json, failure_callback);
                    } else {
                        _success_callback(json, success_callback);
                    }
                })
                .catch((error) => {
                    alert(JSON.stringify(error))
                })
        })
        .catch((error) => {
            alert(error);
        })
}


