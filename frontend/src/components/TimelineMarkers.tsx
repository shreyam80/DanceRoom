export default function TimelineMarkers({comments,duration}:{comments:{comment_id:string;video_timestamp_seconds:number}[];duration:number}){
 return <div className='relative h-2 bg-slate-300 rounded'>{comments.map(c=><div key={c.comment_id} className='absolute top-0 h-2 w-1 bg-red-500' style={{left:`${Math.min(100,(c.video_timestamp_seconds/Math.max(duration,1))*100)}%`}} />)}</div>
}
