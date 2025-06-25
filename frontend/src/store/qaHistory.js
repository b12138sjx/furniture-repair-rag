export default {
  state: {
    history: []
  },
  mutations: {
    ADD_QUESTION_ANSWER(state, { question, answer }) {
      state.history.push({ question, answer, timestamp: new Date() });
    },
    CLEAR_HISTORY(state) {
      state.history = [];
    }
  },
  actions: {
    addQuestionAnswer({ commit }, payload) {
      commit('ADD_QUESTION_ANSWER', payload);
    },
    clearHistory({ commit }) {
      commit('CLEAR_HISTORY');
    }
  },
  getters: {
    allHistory: state => state.history
  }
};