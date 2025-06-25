export default {
  state: {
    documents: []
  },
  mutations: {
    ADD_DOCUMENT(state, document) {
      state.documents.push(document);
    },
    REMOVE_DOCUMENT(state, documentId) {
      state.documents = state.documents.filter(doc => doc.id !== documentId);
    }
  },
  actions: {
    addDocument({ commit }, document) {
      commit('ADD_DOCUMENT', document);
    },
    removeDocument({ commit }, documentId) {
      commit('REMOVE_DOCUMENT', documentId);
    }
  },
  getters: {
    allDocuments: state => state.documents
  }
};