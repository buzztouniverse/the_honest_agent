import { useEffect, useState } from 'react'

// Phone width: the sidebar stays compact, padding shrinks, card headers wrap (narrow.css).
// Keep in step with the breakpoint in narrow.css.
const QUERY = '(max-width: 640px)'

export function useNarrow(): boolean {
  const [narrow, setNarrow] = useState(() => matchMedia(QUERY).matches)
  useEffect(() => {
    const mq = matchMedia(QUERY)
    const update = () => setNarrow(mq.matches)
    mq.addEventListener('change', update)
    return () => mq.removeEventListener('change', update)
  }, [])
  return narrow
}
