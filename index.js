const texto = document.querySelector('input')
const botaoInserir = document.querySelector('.divInsert button')
const botaoDeletarTodos = document.querySelector('.header button')
const ul = document.querySelector('ul')

var todosItens = []

botaoDeletarTodos.onclick = () => {
  todosItens = []
  updateDB()
}

texto.addEventListener('keypress', e => {
  if (e.key == 'Enter' && texto.value != '') {
    setItemDB()
  }
})

botaoInserir.onclick = () => {
  if (texto.value != '') {
    setItemDB()
  }
}

function setItemDB() {
  if (todosItens.length >= 25) {
    alert('Você tem muitos itens na sua lista de tarefas! Já possui mais de 25 tarefas')
    return
  }

  todosItens.push({ 'item': texto.value, 'status': '' })
  updateDB()
}

function updateDB() {
  localStorage.setItem('todolist', JSON.stringify(todosItens))
  loadItens()
}

function loadItens() {
  ul.innerHTML = "";
  todosItens = JSON.parse(localStorage.getItem('todolist')) ?? []
  todosItens.forEach((item, i) => {
    insertItemTela(item.item, item.status, i)
  })
}

function insertItemTela(text, status, i) {
  const li = document.createElement('li')
  
  li.innerHTML = `
    <div class="divLi">
      <button onclick="removeItem(${i})" data-i=${i}><i class='bx bx-dice-6' style='color:#5C5C5C'></i></button>
      <span data-si=${i}>${text}</span>
      <input type="checkbox" class='checkbox-custom' ${status} data-i=${i} onchange="done(this, ${i});" />
    </div>
    `
  ul.appendChild(li)

  if (status) {
    document.querySelector(`[data-si="${i}"]`).classList.add('line-through')
  } else {
    document.querySelector(`[data-si="${i}"]`).classList.remove('line-through')
  }

  texto.value = ''
}

function done(chk, i) {

  if (chk.checked) {
    todosItens[i].status = 'checked' 
  } else {
    todosItens[i].status = '' 
  }

  updateDB()
}

function removeItem(i) {
  todosItens.splice(i, 1)
  updateDB()
}

loadItens()