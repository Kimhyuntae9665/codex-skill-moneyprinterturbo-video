"""One original SDXL text-to-image test on an explicitly supplied NVIDIA GPU."""
import pathlib,time,json,torch,argparse
from diffusers import StableDiffusionXLPipeline
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--out-dir',type=pathlib.Path,required=True)
parser.add_argument('--context',action='store_true',help='Test an independent server-room background')
options=parser.parse_args();R=options.out_dir.resolve();R.mkdir(parents=True,exist_ok=True)
if not torch.cuda.is_available():raise RuntimeError('CUDA is unavailable; do not silently run on CPU')
record={'model':'stabilityai/stable-diffusion-xl-base-1.0','variant':'fp16','device':torch.cuda.get_device_name(0),'torch':torch.__version__,'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'seed':20260905,'steps':25,'width':768,'height':1344,'status':'started'}
prompt='Documentary photograph of a large red circular handwheel valve on a rigid brushed stainless steel pipe, the entire red wheel prominently centered and visible. A single light grey protective work glove gently grips the right side of the red wheel. Dark navy work sleeve. Believable industrial server laboratory with softly blurred server racks behind, detailed machined metal, natural surface imperfections, soft side lighting, clear mechanical connections, vertical close-up composition.'
negative='text, letters, logo, diagram, illustration, cartoon, floating hand, extra fingers, deformed valve, missing wheel, disconnected pipe, plastic toy, split screen, collage'
if options.context:
    prompt='Documentary architectural photograph inside a believable modern data center, a long central aisle between full-height dark server racks, neat cable trays and large fixed stainless cooling pipes overhead, restrained blue and amber status lights, industrial ceiling lights, realistic rubber cables and perforated metal doors, strong perspective and human-scale proportions, a clean floor with subtle reflections, natural neutral colors, detailed but not futuristic, vertical wide composition, no people.'
    negative='text, letters, logo, diagram, illustration, cartoon, sci-fi, futuristic spaceship, plastic toy, split screen, collage, people, floating pipes'
record['scene']='environment' if options.context else 'valve'
record['prompt']=prompt;record['negative_prompt']=negative
start=time.perf_counter()
try:
    pipe=StableDiffusionXLPipeline.from_pretrained(record['model'],torch_dtype=torch.float16,variant='fp16',use_safetensors=True,cache_dir=R/'model-cache',token=False)
    pipe.enable_model_cpu_offload();pipe.vae.enable_tiling()
    record['load_and_download_s']=round(time.perf_counter()-start,3)
    torch.cuda.reset_peak_memory_stats();t=time.perf_counter()
    im=pipe(prompt=prompt,negative_prompt=negative,width=768,height=1344,num_inference_steps=25,guidance_scale=6,generator=torch.Generator('cpu').manual_seed(record['seed'])).images[0]
    torch.cuda.synchronize();record['inference_s']=round(time.perf_counter()-t,3)
    record['peak_allocated_gib']=round(torch.cuda.max_memory_allocated()/1024**3,3)
    im.save(R/('gpu-sdxl-context.png' if options.context else 'gpu-sdxl-valve.png'));record['status']='image_generated'
except Exception as e:
    record['status']='failed';record['error']=str(e);raise
finally:
    record['total_s']=round(time.perf_counter()-start,3)
    (R/('gpu-image-context-report.json' if options.context else 'gpu-image-report.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2),'utf-8')
    print(json.dumps(record,ensure_ascii=False),flush=True)
