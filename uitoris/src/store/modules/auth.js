import { httpServices } from "@/services"
import { userURL, get_tokenURL, refresh_tokenURL } from '@/services/constants';
import router from '@/router/index'
import { TokenService } from "@/services";
const user = JSON.parse(localStorage.getItem('user'));
const initialState = user ? { status: { loggedIn: true }, user } : { status: { loggedIn: false }, user: null }

export const auth = {
    namespaced: true,
    state: initialState,
    actions: {
        Login: async(context, usercredentials) => {
            try {
                const response = await httpServices.login(get_tokenURL, usercredentials);
                console.log(response)
                TokenService.setUser(response.data);
                context.commit('loginSuccess', response.data);
                router.push({ name: 'Production' })
                return Promise.resolve(response);
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.commit('loginFailure');
                context.dispatch('alert/error', message, { root: true });
                return await Promise.reject(error);
            }
        },
        Logout: async(context) => {
            try {
                const response = httpServices.logout();
                context.dispatch('production/clearState', '', { root: true });
                context.dispatch('product/clearState', '', { root: true });
                context.dispatch('order/clearState', '', { root: true });
                context.dispatch('employee/clearState', '', { root: true });
                context.dispatch('plant/clearState', '', { root: true });
                context.commit('logout');

                return await Promise.resolve(response);
            } catch (error) {
                return await Promise.reject(error);
            }
        },

        userRegistration: async(context, userdata) => {
            try {
                const response = await httpServices.register(userURL, userdata);
                context.commit('registerSuccess');
                return await Promise.resolve(response);
            } catch (error) {
                let message = (error.response && error.response.data.detail) || error.message || error.toString();
                context.dispatch('alert/error', message, { root: true });
                context.commit('registerFailure');
                return Promise.reject(error);
            }
        },
        // refreshToken(context, accessToken) {
        //     context.commit('refreshToken', accessToken);
        // },
        getRefreshToken: async(context) => {
            try {
                const response = await httpServices.tokenrefresh(refresh_tokenURL, {
                    refresh: TokenService.getLocalRefreshToken(),
                });
                // console.log(response.data);
                const accessToken = response.data.access;
                context.commit('refreshToken', accessToken);
                TokenService.updateLocalAccessToken(accessToken);
                return Promise.resolve(response)
            } catch (_error) {
                return Promise.reject(_error);
            }
        }
    },
    mutations: {
        loginSuccess(state, user) {
            state.status.loggedIn = true;
            state.user = user;
        },
        loginFailure(state) {
            state.status.loggedIn = false;
            state.user = null;
        },
        logout(state) {
            state.status.loggedIn = false;
            state.user = null;
        },
        registerSuccess(state) {
            state.status.loggedIn = false;
        },
        registerFailure(state) {
            state.status.loggedIn = false;
        },
        refreshToken(state, accessToken) {
            state.status.loggedIn = true;
            state.user = {...state.user, access: accessToken };
        }
    },
}