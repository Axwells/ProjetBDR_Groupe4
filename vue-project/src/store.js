import { reactive } from 'vue';

export const authStore = reactive({
  isLoggedIn: false,
  username: '',
  email: '',
  isSuperUser: false,
  setLoginStatus(isLoggedIn, username = '', email = '', isSuperUser) {
    this.isLoggedIn = isLoggedIn;
    this.username = username;
    this.email = email;
    this.isSuperUser = isSuperUser;
  },
});
