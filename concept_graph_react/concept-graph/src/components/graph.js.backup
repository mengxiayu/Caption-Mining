import * as d3 from 'd3';

import nodes from './data/miserables.json';


var drag = simulation => {
  function dragsubject(event) {
    return simulation.find(event.x, event.y);
  }

  function dragstarted(event) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    event.subject.fx = event.subject.x;
    event.subject.fy = event.subject.y;
  }
  
  function dragged(event) {
    event.subject.fx = event.x;
    event.subject.fy = event.y;
  }
  
  function dragended(event) {
    if (!event.active) simulation.alphaTarget(0);
    event.subject.fx = null;
    event.subject.fy = null;
  }
  
  return d3.drag()
      .subject(dragsubject)
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended);
}

var color = () => {
  const scale = d3.scaleOrdinal(d3.schemeCategory10);
  return d => scale(d.group);
}

var chart = () => {
  const links = data.links.map(d => Object.create(d));
  const nodes = data.nodes.map(d => Object.create(d));

  const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id))
      .force("charge", d3.forceManyBody())
      .force("center", d3.forceCenter(width / 2, height / 2));

  const context = DOM.context2d(width, height);

  simulation.on("tick", ticked);

  invalidation.then(() => simulation.stop());

  return d3.select(context.canvas).call(drag(simulation)).node();
  
  
  function ticked() {
    context.clearRect(0, 0, width, height);

    context.beginPath();
    links.forEach(drawLink);
    context.strokeStyle = "#aaa";
    context.stroke();

    context.strokeStyle = "#fff";
    for (const node of nodes) {
      context.beginPath();
      drawNode(node) 
      context.fillStyle = color(node);
      context.fill();
      context.stroke();
    }
  }
  
  function drawLink(d) {
    context.moveTo(d.source.x, d.source.y);
    context.lineTo(d.target.x, d.target.y);
  }

  function drawNode(d) {
    context.moveTo(d.x + 3, d.y);
    context.arc(d.x, d.y, 3, 0, 2 * Math.PI);
  }
}