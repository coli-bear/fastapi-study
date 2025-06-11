import {writable} from 'svelte/store'

const persist_storage = (key, initValue) => {
 const storedValueStr = localStorage.getItem(key)
    const parsed = storedValueStr != null ? JSON.parse(storedValueStr) : initValue;
    const store = writable(parsed);
    store.subscribe((val) => {
        localStorage.setItem(key, JSON.stringify(val))
    })
    return store
}

export const page = persist_storage("page", 0)
export const access_token = persist_storage("access_token", "")
export const username = persist_storage("username", "")
export const is_signed = persist_storage("is_signed", false)