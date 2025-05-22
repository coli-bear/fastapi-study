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
    if (success_callback) {
        success_callback(json)
    }
}

export const fastapi = (operation, url, params, success_callback, failure_callback) => {
    let method = operation;
    let content_type = 'application/json';
    let _url = _generate_url(method, url, params);
    let options = {
        method: method,
        headers: {
            'Content-Type': content_type,
            'Accept': content_type
        }
    }


    fetch(_url, options)
        .then((response) => {
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


