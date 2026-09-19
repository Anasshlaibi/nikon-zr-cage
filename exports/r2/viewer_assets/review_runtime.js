
(()=>{
const stage=document.getElementById('stage'),label=document.getElementById('selection');
try{
const scene=new THREE.Scene();scene.background=new THREE.Color('#eef0f2');
const camera=new THREE.PerspectiveCamera(36,1,.1,3000);camera.up.set(0,0,1);camera.position.set(250,320,230);
const renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.outputEncoding=THREE.sRGBEncoding;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.1;stage.prepend(renderer.domElement);
const controls=new THREE.OrbitControls(camera,renderer.domElement);controls.target.set(0,0,42);controls.enableDamping=true;controls.minDistance=70;controls.maxDistance=850;
scene.add(new THREE.HemisphereLight(0xe7eef5,0x727078,.55));
for(const [x,y,z,intensity] of [[140,180,350,.85],[-250,80,150,.65],[50,-220,300,.9]]){const l=new THREE.DirectionalLight(0xffffff,intensity);l.position.set(x,y,z);scene.add(l);}
const data=JSON.parse(document.getElementById('model-data').textContent), meshes=[];
const colors={metal:0x070a0e,steel:0x858f9c,rubber:0x060809,camera:0xd4d9df,glass:0x151c25,accent:0xb72d27};
for(const p of data){
 const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.Float32BufferAttribute(p.vertices.flat(),3));geo.setIndex(p.triangles.flat());geo.computeVertexNormals();
 const mat=new THREE.MeshStandardMaterial({color:colors[p.material],metalness:p.material==='steel'?.65:p.material==='metal'?.32:0,roughness:p.material==='rubber'?.78:.42});
 const mesh=new THREE.Mesh(geo,mat);mesh.userData=p;scene.add(mesh);meshes.push(mesh);
}
function update(){
 const showCamera=document.getElementById('camera').checked,showGrip=document.getElementById('grip').checked,explode=document.getElementById('explode').checked;
 for(const m of meshes){const p=m.userData;m.visible=p.group==='core'||p.group==='lens'||(p.group==='camera'&&showCamera)||(p.group==='grip'&&showGrip);m.position.set(...(explode&&p.group!=='camera'?p.explode:[0,0,0]));}
 label.textContent=(showGrip?'59':'53')+'-part assembly'+(showCamera?' + camera proxy':'');
}
for(const id of ['camera','grip','explode'])document.getElementById(id).addEventListener('change',update);
document.getElementById('view').addEventListener('change',e=>{const poses={perspective:[250,320,230],front:[0,420,42],rear:[0,-420,42],left:[-420,0,42],top:[0,.1,470]};camera.position.set(...poses[e.target.value]);controls.target.set(0,0,42);controls.update();});
const ray=new THREE.Raycaster(),pointer=new THREE.Vector2();
renderer.domElement.addEventListener('pointermove',e=>{if(e.buttons)return;const rect=renderer.domElement.getBoundingClientRect();pointer.set(2*(e.clientX-rect.left)/rect.width-1,1-2*(e.clientY-rect.top)/rect.height);ray.setFromCamera(pointer,camera);const hit=ray.intersectObjects(meshes.filter(m=>m.visible),false)[0];if(hit)label.textContent=hit.object.userData.name.replaceAll('_',' ');});
function resize(){const w=stage.clientWidth,h=stage.clientHeight;camera.aspect=w/h;camera.updateProjectionMatrix();renderer.setSize(w,h);}
new ResizeObserver(resize).observe(stage);resize();update();controls.update();
function frame(){requestAnimationFrame(frame);controls.update();renderer.render(scene,camera);}frame();
window.zrReview={scene,camera,meshes,renderer,controls};
}catch(e){const el=document.getElementById('error');el.style.display='block';el.textContent='3D viewer could not start: '+e.message+' — the STEP and GLB files remain available.';console.error(e);}
})();
