import { useRef } from 'react';
export default function VideoPlayer({src,onTimeUpdate,onLoadedMetadata}:{src:string;onTimeUpdate:(t:number)=>void;onLoadedMetadata?:(d:number)=>void}){
 const ref=useRef<HTMLVideoElement>(null);
 return <video ref={ref} controls className='w-full rounded bg-black' src={src} onTimeUpdate={(e)=>onTimeUpdate(e.currentTarget.currentTime)} onLoadedMetadata={(e)=>onLoadedMetadata?.(e.currentTarget.duration)} />
}
