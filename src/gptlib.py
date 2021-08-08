import gpt_2_simple as gpt2
import tensorflow as tf
import logging
from datetime import datetime, timezone
import gc

sess = None

def start_sess(run_name):
    global sess
    global session_generated
    global current_run_name

    if not sess is None:
        logging.info(f'{datetime.now(timezone.utc)} Restarting tf session')
        tf.compat.v1.reset_default_graph()
        sess.close()

    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess, run_name=run_name)
    session_generated = 0
    current_run_name = run_name

async def generate(prefix, callback):
    global session_generated
    global current_run_name

    text = gpt2.generate(sess, 
        run_name=current_run_name,
        top_k=20,
        nsamples=1,
        batch_size=1,
        temperature=1.4,
        length = 150,
        prefix = prefix,
        return_as_list=True
                )[0]
    # Replace code marks with a version with invisible spaces
    text = text.replace('```', '`​`​`')
    await callback(f'```{text}```')

    session_generated += 1

    if session_generated >= 2:
        start_sess(current_run_name)

    logging.info(f'{datetime.now(timezone.utc)} Uncollectable garbage count: {len(gc.garbage)}')
    gc.collect()
