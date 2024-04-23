import { defineStore } from 'pinia'

// export const useUserStore = defineStore({
//   id: 'user', 
//   state: () => {
//     return {
//       name: '雷猴'
//     }
//   },
//   getters: {
//     fullName: (state) => {
//       return '我叫 ' + state.name
//     }
//   },
//   actions: {
//     updateName(name) {
//       this.name = name
//     }
//   }
// })

export const recommendationStore = defineStore({
  id: 'recommend', 
  state: () => ({
    data:'',
  }),
  getters: {
  },
  actions: {
    updateData(data) {
      this.data = data
    }
  }
})
