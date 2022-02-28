import {
  BrowserRouter as Router,
  Routes,
  Route,
  // Link
} from "react-router-dom";

import logo from './logo.svg';
import './App.css';
import Layout from './pages/Layout';
import { ForceGraph } from './components/force_graph_svg';
// import { FileSelect } from './components/file_select';

import data_cs241 from './data/course_concepts_CS_241.json';
import data_cs410 from './data/course_concepts_CS_410.json';
import data_test from './data/course_concepts.json';
// import data from './graph_data/contexts';



function App() {
  return (
    <div className="App">
      <header className="App-header">
        {/* <img src={logo} className="App-logo" alt="logo" /> */}
      </header>

      <div>
        <nav className='Nav'>
          <Router>
            <Routes>
              <Route path="/" element={<Layout />}>
                <Route index element={<Home />} />
                <Route path="CS241" element={<CS241 />} />
                <Route path="CS410" element={<CS410 />} />
                <Route path="test" element={<Test />} />
              </Route>
            </Routes>
          </Router>
        </nav>


        {/* <ForceGraph
          nodesData={data}
          nodeHoverTooltip={0} /> */}


      </div>
    </div>
  );
}


function Home() {
  return <h2>Home</h2>;
}

function About() {
  return <h2>About</h2>;
}

function Users() {
  return <h2>Users</h2>;
}

function CS241() {
  return <ForceGraph
    nodesData={data_cs241}
    nodeHoverTooltip={0} />;
}

function CS410() {
  return <ForceGraph
    nodesData={data_cs410}
    nodeHoverTooltip={0} />;
}

function Test() {
  return <ForceGraph
    nodesData={data_test}
    nodeHoverTooltip={0} />;
}

export default App;
