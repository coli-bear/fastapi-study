import qs from "qs"
import {access_token, username, is_signed} from "./store.js";
import {get} from "svelte/store";
import {push} from "svelte-spa-router";

function _generate_url(method, url, params) {
    let _url = `${import.meta.env.VITE_SERVER_URL}${url.startsWith('/') ? url : '/' + url}`;
    if (method.toLowerCase() === 'get' && params && Object.keys(params).length > 0) {
        const queryString = new URLSearchParams(params).toString();
        _url += '?' + queryString;
    }
    return _url;
}

const _is_error = (response) => {
    if (response) {
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

function _is_authentication_error(method, status) {
    return method !== 'signin' && (status === 401 || status === 403);
}

function unauthorized_callback() {
    access_token.set('');
    username.set('');
    is_signed.set(false);
    alert('Authentication error, please sign in again.');
    push('/signin');
}

function default_options(method, params, content_type = 'application/json') {
    let options = {
        method: method,
        headers: {
            'Content-Type': content_type,
            'Accept': content_type
        }
    }

    const _access_token = get(access_token);
    if (_access_token) {
        options.headers['Authorization'] = `Bearer ${_access_token}`;
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

            if (response.status === 204) {
                _success_callback(undefined, success_callback)
                return
            }

            response
                .json()
                .then((json) => {
                    if (_is_authentication_error(method, response.status)) {
                        _failure_callback(json, unauthorized_callback)
                    } else if (_is_error(response)) {
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


