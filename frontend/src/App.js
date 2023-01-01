import logo from './logo.png';
import './App.css';
import List from './livros/Lista';



function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
        Momentum, Sua biblioteca online para Classificações, Críticas e Onde ver os Melhores livros e livro que tornaram Filmes
        </p>      
      </header>

      <List/>
    </div>
  );
}

export default App;
