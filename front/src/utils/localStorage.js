/**
 * 保存到localStorage数据操作
 * 员工信息的保存
 */
export const getCaCheSession = (() => {
    return localStorage.getItem('session') || ''
})

export const setCaCheSession = ((token) => {
    return localStorage.setItem('session', token)
})

export const getCaCheAcc = (() => {
    return localStorage.getItem('acc')
})

export const setCaCheAcc = ((acc) => {
    return localStorage.setItem('acc', acc)
})

export const setCaCheEmail = ((email) => {
    return localStorage.setItem('email', email)
})

export const getCaCheEmail = (() => {
    return (localStorage.getItem('email') || '').toString()
})

export const getCaCheName = (() => {
    return (localStorage.getItem('name') || '').toString()
})

export const setCaCheName = ((name) => {
    return localStorage.setItem('name', name)
})


export const getCaCheRoleType = (() => {
    return localStorage.getItem('roleType')
})

export const setCaCheRoleType = ((roleType) => {
    return localStorage.setItem('roleType', roleType)
})



