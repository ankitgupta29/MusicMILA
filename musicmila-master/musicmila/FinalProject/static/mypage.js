jQuery(document).ready(function() {  
									 
                                 var myPlaylist = new jPlayerPlaylist({
									jPlayer: "#jquery_jplayer_N",
									cssSelectorAncestor: "#jp_container_N"
										}, [
											{
												title:"Cro Magnon Man",
												artist:"The Stark Palace",
												mp3:"http://www.jplayer.org/audio/mp3/TSP-01-Cro_magnon_man.mp3",
												poster: "http://www.jplayer.org/audio/poster/The_Stark_Palace_640x360.png"
											}
										], {
											playlistOptions: {
												enableRemoveControls: true
											},
											swfPath: "http://jplayer.org/latest/js",
											supplied: "webmv, ogv, m4v, oga, mp3",
											smoothPlayBar: true,
											keyEnabled: true,
											autoPlay: true,
											audioFullScreen: true
										});
										jQuery("#playlist-setPlaylist-audio-mix").click(function() {
											myPlaylist.setPlaylist([
												{
													title:"Cro Magnon Man",
													artist:"The Stark Palace",
													mp3:"http://www.jplayer.org/audio/mp3/TSP-01-Cro_magnon_man.mp3",
													oga:"http://www.jplayer.org/audio/ogg/TSP-01-Cro_magnon_man.ogg",
													poster: "http://www.jplayer.org/audio/poster/The_Stark_Palace_640x360.png"
												}
												]);
												});
										
										jQuery("#playlist-remove").click(function() {
													myPlaylist.remove();
												});
										jQuery("#playlist-shuffle").click(function() {
													myPlaylist.shuffle();
												});
										jQuery("#playlist-next").click(function() {
													myPlaylist.next();
												});
										jQuery("#playlist-previous").click(function() {
													myPlaylist.previous();
												});
										jQuery("#playlist-play").click(function() {
													myPlaylist.play();
												});
										jQuery("#playlist-pause").click(function() {
												myPlaylist.pause();
												});
										jQuery("#playlist-option-autoPlay-true").click(function() {
													myPlaylist.option("autoPlay", true);
												});
										jQuery("#playlist-option-autoPlay-false").click(function() {
													myPlaylist.option("autoPlay", false);
												});
										jQuery("#playlist-option-displayTime-slow").click(function() {
													myPlaylist.option("displayTime", "slow");
												});
										
                                         
	                                }); //close of main jquery function
