const getElement = (selector) => {
  const element = document.querySelector(selector)
  if (element) return element
}

const links = getElement('.nav-links')
const userLinks = getElement('.user-data')
const navBtnDOM = getElement('.nav-btn')
navBtnDOM.addEventListener('click', () => {
  links.classList.toggle('show-links')
  userLinks.classList.toggle('show-links')
})
