import { mount } from 'svelte'
import App from './App.svelte'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'

const app = mount(App, {
  target: document.getElementById('app'),
})

export default app
