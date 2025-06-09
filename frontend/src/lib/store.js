import {writable} from 'svelte/store'

const persist_storage = (key, initValue) => {
    const storedValueStr = localStorage.getItem(key)
    const parsed = storedValueStr != null ? JSON.parse(storedValueStr) : initValue;
    const store = writable(typeof parsed === 'number' ? parsed : Number(parsed));
    store.subscribe((val) => {
        localStorage.setItem(key, JSON.stringify(val))
    })
    return store
}

export const page = persist_storage("page", 0)