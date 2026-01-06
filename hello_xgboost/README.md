install requires libomp i.e. `brew install libomp`

## Notes

### Caching the Model

Model storage (`save_model`, useful for long-term storage) is different than memory storage (`pickle`, useful for checkpointing). [Introduction to Model IO](https://xgboost.readthedocs.io/en/stable/tutorials/saving_model.html#introduction-to-model-io)

**Model storage** i.e. `model.save_model(file.json)`

> We guarantee backward compatibility for models but not for memory snapshots.
>
> Models (trees and objective) use a stable representation, so that models produced in earlier versions of XGBoost are accessible in later versions of XGBoost. If you’d like to store or archive your model for long-term storage, use `save_model` (Python)
> [link](https://xgboost.readthedocs.io/en/stable/tutorials/saving_model.html#a-note-on-backward-compatibility-of-models-and-memory-snapshots)

**Memory snapshot** i.e. `pickle.dump`

> memory snapshot (serialisation) captures many stuff internal to XGBoost, and its format is not stable and is subject to frequent changes. Therefore, memory snapshot is suitable for checkpointing only, where you persist the complete snapshot of the training configurations so that you can recover robustly from possible failures and resume the training process.
> [link](https://xgboost.readthedocs.io/en/stable/tutorials/saving_model.html#a-note-on-backward-compatibility-of-models-and-memory-snapshots)
