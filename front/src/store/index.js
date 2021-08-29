import Vue from 'vue'
import Vuex from 'vuex'


Vue.use(Vuex);


const state = {
    userName:'',
    loading:false,
    userNameIsChange:false,
    roleType:''
};

const mutations = {
    setUserName(state, userName){
        state.userName = userName;
    },
    setLoading(state, loading){
        state.loading = loading;
    },
    setUserNameIsChange(state, userNameIsChange){
        state.userNameIsChange = userNameIsChange;
    },

    setRoleType(state,  roleType){
        state.roleType = roleType;
    },

    RESET(state, sign){
        state.userName = ''
        state.roleType = ''
        state.loading = false
        state.userNameIsChange = true
    }

};

const getters = {
    getUserName(state) {
        return state.userName
    },
    getLoading(state){
        return state.loading
    },
    getRoleType(state){
        return state.roleType
    },
    getUserNameIsChange(state){
        return state.userNameIsChange
    }
};

const actions = {
  //这里面的方法是用来异步触发mutations里面的方法,context与store 实例具有相同方法和属性
  RESET({ commit }, sign) {
    commit("RESET", sign);
    localStorage.clear()
  }
};

const store = new Vuex.Store({
    state,
    getters,
    mutations,
    actions
});


export default store
