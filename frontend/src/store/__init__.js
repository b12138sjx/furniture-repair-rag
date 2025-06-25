import { createStore } from 'vuex'
import knowledge from './knowledge'
import qaHistory from './qaHistory'

const store = createStore({
  modules: {
    knowledge,
    qaHistory
  }
})

export default store