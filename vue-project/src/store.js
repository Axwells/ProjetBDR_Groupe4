import { reactive } from 'vue';

export const authStore = reactive({
  isLoggedIn: false,
  username: '',
  email: '',
  setLoginStatus(isLoggedIn, username = '', email = '') {
    this.isLoggedIn = isLoggedIn;
    this.username = username;
    this.email = email;
  },
});
