
export default {
  state: {
    running: false,
    source_image: null,
    target_image: null,
  },
  getters: {
  },
  mutations: {
    updateRunning(state, running){
        state.running = running
    },
    updateImage(state, image){
        state.source_image = image.source_image
        state.target_image = image.target_image
    }
  },
  actions: {
  },
  modules: {
  }
}
