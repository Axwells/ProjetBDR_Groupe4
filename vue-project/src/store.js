import { reactive } from 'vue';

export const authStore = reactive({
  isLoggedIn: false,
  username: '',
  setLoginStatus(isLoggedIn, username = '') {
    this.isLoggedIn = isLoggedIn;
    this.username = username;
  },
});
