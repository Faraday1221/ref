# 30 seconds to Keras with Comments
The following is slightly modified to fit <THE ?? DATASET> from the [keras.io](keras.io) introduction tutorial with a few additional comments

note: I'm using the Theano backend i.e.

    cat ~/.keras/keras.json
    {
        "image_dim_ordering": "tf",
        "epsilon": 1e-07,
        "floatx": "float32",
        "backend": "theano"
    }


### Keras Tutorial
    from keras.models import Sequential
    # Sequential is the main type of model, a linear stack of layers

    model = Sequential()

    from keras.layers import Dense, Activation
    #
    model.add(Dense(output_dim=64, input_dim=100))
    model.add(Activation("relu"))
    model.add(Dense(output_dim=10))
    model.add(Activation("softmax"))

### Sequential
Linear stack of layers. Takes arguments layers: list of layers to add to the model. Layers are added with the `.add()` method.

> Note:
>    The first layer passed to a Sequential model
    should have a defined input shape. What that
    means is that it should have received an `input_shape`
    or `batch_input_shape` argument,
    or for some type of layers (recurrent, Dense...)
    an `input_dim` argument.

For Example

```python
    model = Sequential()
    # first layer must have a defined input shape
    model.add(Dense(32, input_dim=500))
    # afterwards, Keras does automatic shape inference
    model.add(Dense(32))

    # also possible (equivalent to the above):
    model = Sequential()
    model.add(Dense(32, input_shape=(500,)))
    model.add(Dense(32))

    # also possible (equivalent to the above):
    model = Sequential()
    # here the batch dimension is None,
    # which means any batch size will be accepted by the model.
    model.add(Dense(32, batch_input_shape=(None, 500)))
    model.add(Dense(32))
```

### Dense
Dense is 'just your regular fully connected NN layer.' e.g.

```python
    # as first layer in a sequential model:
    model = Sequential()
    model.add(Dense(32, input_dim=16))
    # now the model will take as input arrays of shape (*, 16)
    # and output arrays of shape (*, 32)

    # this is equivalent to the above:
    model = Sequential()
    model.add(Dense(32, input_shape=(16,)))

    # after the first layer, you don't need to specify
    # the size of the input anymore:
    model.add(Dense(32))
```
### Activation
Activation specifies the activation function for the layer. The available activation functions are found in `keras.activations`. The available activation functions are:

    K                elu              get_from_module  linear           sigmoid          softplus         tanh
    absolute_import  get              hard_sigmoid     relu             softmax          softsign
