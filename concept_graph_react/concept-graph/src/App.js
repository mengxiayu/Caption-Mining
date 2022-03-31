import {
  BrowserRouter as Router,
  Routes,
  Route,
  // Link
} from "react-router-dom";

import logo from './logo.svg';
import './App.css';
import Layout from './pages/Layout';
import { ForceGraphConcept } from './components/force_graph_concept';
import { ForceGraphTopics } from './components/force_graph_topics';
// import { FileSelect } from './components/file_select';

import data_cs241 from './data/course_concepts_CS_241.json';
import data_cs410 from './data/course_concepts_CS_410.json';
import data_test from './data/course_concepts.json';
// import data from './graph_data/contexts';

import topic_data_cs410 from './data/topic_graph/topic_graph_CS410.json'


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
                <Route path="TopicsCS410" element={<TopicsCS410 />} />
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
  return <ForceGraphConcept
    nodesData={data_cs241}
    nodeHoverTooltip={0} />;
}

function CS410() {
  return <ForceGraphConcept
    nodesData={data_cs410}
    nodeHoverTooltip={0} />;
}

function Test() {
  return <ForceGraphConcept
    nodesData={data_test}
    nodeHoverTooltip={0} />;
}

function TopicsCS410() {
  return <ForceGraphTopics
    nodesData={topic_data_cs410}
    nodeHoverTooltip={0} />;
}

export default App;
