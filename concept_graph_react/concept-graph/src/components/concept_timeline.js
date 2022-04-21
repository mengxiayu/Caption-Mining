import React from "react";
import $ from 'jquery';

import videojs from "video.js";
import "./video-js.css";
import * as m from "videojs-markers/dist/videojs-markers.js";
import "videojs-markers/dist/videojs.markers.css";

import testVideo from ".././videos/test_21_min.mp4";

export function ConceptTimeline() {
    const playerRef = React.useRef(null);

    const videoJsOptions = { // lookup the options in the docs for more options
        // autoplay: true,
        controls: true,
        responsive: true,
        fluid: true,
        sources: [{
            src: testVideo,
            type: 'video/mp4'
        }]
    }

    const handlePlayerReady = (player) => {
        playerRef.current = player;

        // you can handle player events here
        player.on('waiting', () => {
            console.log('player is waiting');
        });

        player.on('dispose', () => {
            console.log('player will dispose');
        });
    };

    return (
        <>
            <div ref={playerRef} className='videoHolder'>
                <VideoJS options={videoJsOptions} onReady={handlePlayerReady} />
            </div>;
        </>
    )
}


export const VideoJS = (props) => {

    const videoRef = React.useRef(null);
    const playerRef = React.useRef(null);
    const { options, onReady } = props;

    React.useEffect(() => {
        // make sure Video.js player is only initialized once
        if (!playerRef.current) {
            const videoElement = videoRef.current;
            if (!videoElement) return;

            const player = playerRef.current = videojs(videoElement, options, () => {
                console.log("player is ready");
                onReady && onReady(player);
            });

            player.markers({
                markerStyle: {
                    'width': '3px',
                    'height': '8px',
                    'border-radius': '30%',
                    'background-color': 'rgb(255 113 0)',
                    'font-size': '20px',
                },
                markerTip: {
                    display: true,
                    text: function (marker) {
                        return marker.text;
                    },
                    time: function (marker) {
                        return marker.time;
                    }
                },
                breakOverlay: {
                    display: true,
                    displayTime: 3,
                    style: {
                        'width': '100%',
                        'height': '20%',
                        'background-color': 'rgba(0,0,0,0.7)',
                        'color': 'white',
                        // 'font-size': '10px'
                    },
                    text: function (marker) {
                        return marker.overlayText;
                    }
                },
                onMarkerClick: function (marker) { },
                onMarkerReached: function (marker) { },
                markers: [
                    {
                        time: 1 * 60,
                        text: "Concepts: linked list",
                        overlayText: "ok so let , build , a web client so this be not go to be quite as good as firefox or chrome but i promise , that , be a lot fresh and also a lot small there be just one little downside which be that if , want to navigate to a different page , be go to have to recompile , but nevermind , be for a technical audience anyway so here , go , want to build a web server and , want to specify name like illinois dot edu and , need to convert that there into a tcp address right for that here be a really really useful function getaddressinfo in fact , do many thing but , be go to use , today to create the information , need to create a socket and also to call connect and so , eventually will get back a family a socket type and address length and and address as well so , will use these to kind of",
                        class: 'custom-marker'
                    },
                    {
                        time: 2 * 60,
                        text: "Concepts: linked list",
                        overlayText: "ok so let , build , a web client so this be not go to be quite as good as firefox or chrome but i promise , that , be a lot fresh and also a lot small there be just one little downside which be that if , want to navigate to a different page , be go to have to recompile , but nevermind , be for a technical audience anyway so here , go , want to build a web server and , want to specify name like illinois dot edu and , need to convert that there into a tcp address right for that here be a really really useful function getaddressinfo in fact , do many thing but , be go to use , today to create the information , need to create a socket and also to call connect and so , eventually will get back a family a socket type and address length and and address as well so , will use these to kind of",
                        class: 'custom-marker'
                    },
                    {
                        time: 5 * 60,
                        text: "Concepts: return value; void pointer; thread exit",
                        overlayText: "actually set up one of these struct as a as like as a hint to say this be the kind of stuff , need and then , create another one for , in fact a potentially a link list of way that , can actually connect to that server so what , need in here ok let , scroll down be , be go to call getaddressinfo , be go to pass in host and the port that would like to connect to this can either be a number but , have to be a string otherwise , get a segfault or , can be a name like https for example but here be where , go to pass a pointer to an exist struct and then here be where , pass in",
                        class: 'custom-marker'
                    },
                    {
                        time: 6 * 60,
                        text: "Concepts: return value; void pointer; thread exit",
                        overlayText: "create some heap memory for , with the result so that be what , need to get to let , think about how , can set up this hint object what do that look like okay so here be the plan , get to say what kind of connection , want do , want to say an ip four or maybe six or both do , want to set up a client or perhaps , want to set up a server so , be go to have to set those flag there be many thing in here however that , do not currently need and so the first thing that , should do be actually take , hint object so here , be ok and zero , all out ok so take the address of , and the number of byte that i need for this struct will be",
                        class: 'custom-marker'
                    },
                    {
                        time: 12 * 60,
                        text: "Concepts: web server; web page; ip address",
                        overlayText: "create some heap memory for , with the result so that be what , need to get to let , think about how , can set up this hint object what do that look like okay so here be the plan , get to say what kind of connection , want do , want to say an ip four or maybe six or both do , want to set up a client or perhaps , want to set up a server so , be go to have to set those flag there be many thing in here however that , do not currently need and so the first thing that , should do be actually take , hint object so here , be ok and zero , all out ok so take the address of , and the number of byte that i need for this struct will be",
                        class: 'custom-marker'
                    },                    
                    {
                        time: 15 * 60,
                        text: "Concepts: web server; web page; ip address",
                        overlayText: "to zero so memset be go to walk through all of those byte set , all to zero so if i do not set some of the all of the parameter inside that field sorry inside that struct then by default , will have a value of zero which be a good thing the other thing , be go to need in here be a pointer to result as well so i do not need an addressinfo i just need a pointer to one right so , can start to set this up now if , be go to set up a tcp then the address family i need be af address family and i need inet which mean ip version four i net short for internet if , want ip version six then , would use af inet underscore six there be also inet_any if , want to say i do not care",
                        class: 'custom-marker'
                    },
                    {
                        time: 16 * 60,
                        text: "Concepts: web server; web page; ip address",
                        overlayText: "about try to get an ip four address right and what kind of socket type well this be where , can say i actually want either udp or tcp and the constant here either d gram for a datagram udp or stream for a tcp so , be go to use stream i will look up the correct name for this at a moment from a man page but , be something like sock stream yes in fact this what be soccer underscore stream ok so , have say about hint that sufficient for what , need for , little client here so now let , say go get address info please and , 'd like to connect on port eighty because that be where unencrypte web",
                        class: 'custom-marker'
                    },
                    {
                        time: 16 * 60,
                        text: "Concepts: web server; web page; ip address",
                        overlayText: "about try to get an ip four address right and what kind of socket type well this be where , can say i actually want either udp or tcp and the constant here either d gram for a datagram udp or stream for a tcp so , be go to use stream i will look up the correct name for this at a moment from a man page but , be something like sock stream yes in fact this what be soccer underscore stream ok so , have say about hint that sufficient for what , need for , little client here so now let , say go get address info please and , 'd like to connect on port eighty because that be where unencrypte web",
                        class: 'custom-marker'
                    },
                    {
                        time: 17 * 60,
                        text: "Concepts: web server; web page; ip address",
                        overlayText: "and here be the address of , result pointer which be go to be change as well ok so will getaddressinfo change , result pointer who know to be sure , well actually check to see whether the getaddressinfo actually succeed or not so , be important with all of these network call to check , return value so if , do not succeed then , result pointer can be point to anything game because , never set , maybe , be point to this smiley over here so a little bit more of a bus code would have actually explicitly set result equal to zero but certainly , do not want to assume that , be be set unless getaddressinfo return zero so if , do not return zero then , actually have a useful error function down here ga - get address info gai - underscore st",
                        class: 'custom-marker'
                    },
                    {
                        time: 18 * 60,
                        text: "Concepts: web server; web page; ip address",
                        overlayText: "to why this occur so , do not use errno this be one of the few time that be not use errno to find out what happen instead the error be actually encode by the return value directly ok so , have get , getaddressinfo now , can make the call for a socket to connect so rather than do that here let , actually do that as part of the live code so , can start write this ok right so yeah i be right the socket type with sock underscore stream so great , have get that now , be time to actually make , connection ok so i want to make , a socket so let , have a why , ok that be fix the indenting here right ok so let , have",
                        class: 'custom-marker'
                    }
                ]
            });

        } else {
            // you can update player here [update player through props]
            // const player = playerRef.current;
            // player.autoplay(options.autoplay);
            // player.src(options.sources);
        }
    }, [options, videoRef]);

    // Dispose the Video.js player when the functional component unmounts
    React.useEffect(() => {
        const player = playerRef.current;

        return () => {
            if (player) {
                player.dispose();
                playerRef.current = null;
            }
        };
    }, [playerRef]);

    return (
        <div data-vjs-player>
            <video ref={videoRef} className="video-js vjs-big-play-centered" />
        </div>
    );
}