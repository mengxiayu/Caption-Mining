import React from "react";

import * as d3 from 'd3';

export function ForceGraph({ nodesData, nodeHoverTooltip }) {
    const containerRef = React.useRef(null);

    React.useEffect(() => {
        let destroyFn;

        const { destroy } = getForceGraph(containerRef.current, nodesData, nodeHoverTooltip);
        destroyFn = destroy;

        return destroyFn;
    }, []);

    return <div ref={containerRef} className='container' />;
}

function getForceGraph(
    container,
    nodesData,
    nodeHoverTooltip,
) {
    const links = nodesData.links.map((d) => Object.assign({}, d));
    const nodes = nodesData.nodes.map((d) => Object.assign({}, d));

    const containerRect = container.getBoundingClientRect();
    const height = containerRect.height;
    const width = containerRect.width;

    const color = (d) => {
        const group2color = [
            "rgb(78, 121, 167)", "rgb(225, 87, 89)", "rgb(89, 161, 79)"
        ]; // course, lecture, concepts

        return group2color[d.group];
    };

    const icon = (d) => {
        // return d.gender === "male" ? "m" : "f";
        return d.id;
    }

    const getClass = (d) => {
        const group2class = [
            "course", "lecture", "concepts"
        ];
        return group2class[d.group];
    };

    function drag(simulation) {
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
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended);
    };



    const simulation = d3
        .forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(d => d.id))
        .force("charge", d3.forceManyBody().strength(-1000))
        .force("x", d3.forceX())
        .force("y", d3.forceY());

    const svg = d3
        .select(container)
        .append("svg")
        .attr("viewBox", [-width / 2, -height / 2, width, height])
    // .call(d3.zoom().on("zoom", function () {
    //     svg.attr("transform", d3.zoomTransform(this));
    // }));

    const link = svg
        .append("g")
        .attr("stroke", "#999")
        .attr("stroke-opacity", 0.6)
        .selectAll("line")
        .data(links)
        .join("line")
        .attr("stroke-width", d => Math.sqrt(d.value));

    const node = svg
        .append("g")
        .attr("stroke", "#fff")
        .attr("stroke-width", 2)
        .selectAll("circle")
        .data(nodes)
        .join("circle")
        .attr("r", 18)
        .attr("fill", color)
        .call(drag(simulation));

    const label = svg.append("g")
        .attr("class", "labels")
        .selectAll("text")
        .data(nodes)
        .enter()
        .append("text")
        .attr('text-anchor', 'middle')
        .attr('dominant-baseline', 'central')
        .attr("class", d => `fa ${getClass(d)}`)
        .text(d => { return icon(d); })
        .call(drag(simulation));

    simulation.on("tick", () => {
        //update link positions
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        // update node positions
        node
            .attr("cx", d => d.x)
            .attr("cy", d => d.y);

        // update label positions
        label
            .attr("x", d => { return d.x; })
            .attr("y", d => { return d.y; })
    });

    return {
        destroy: () => {
            simulation.stop();
        },
        nodes: () => {
            return svg.node();
        }
    };
}

