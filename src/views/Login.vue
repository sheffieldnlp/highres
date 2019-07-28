<template>
    <section class="hero is-primary is-fullheight login">
        <div class="hero-body">
            <div class="container has-text-centered">
                <div class="column is-4 is-offset-4">
                    <h3 class="title has-text-white">Login</h3>
                    <p class="subtitle">Please login to proceed to admin page.</p>
                    <div class="box">
                        <div class="field">
                            <div class="control">
                                <input class="input is-large"
                                       type="email" v-model="input.email"
                                       placeholder="Your Email" autofocus="">
                            </div>
                        </div>
                        <div class="field">
                            <div class="control">
                                <input class="input is-large"
                                       type="password" v-model="input.password"
                                       placeholder="Your Password">
                            </div>
                        </div>
                        <button type="button"
                                    class="button is-block is-info is-large is-fullwidth"
                                    v-on:click="login()">Login</button>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
import { EventBus } from '../utils';

export default {
  name: 'Login',
  data() {
    return {
      input: {
        email: '',
        password: '',
      },
    };
  },
  methods: {
    login() {
      if (this.input.email !== '' && this.input.password !== '') {
        this.$store.dispatch('login', {
          email: this.input.email,
          password: this.input.password,
        })
          .then(() => this.$router.push({ name: 'admin' }))
          .catch((error) => {
            console.log(error);
          });
      }
    },
  },
  mounted() {
    EventBus.$on('failedAuthentication', () => {
      this.$toast.open({
        message: 'Email or password does not exist!',
        type: 'is-danger',
      });
    });
  },
};
</script>

<style scoped>
.login {
  font-size: 14px;
  font-weight: 300;
}
.box {
  margin-top: 5rem;
}
input {
  font-weight: 300;
}
p {
  font-weight: 700;
}
p.subtitle {
  padding-top: 1rem;
}
</style>
