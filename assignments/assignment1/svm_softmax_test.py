import random
from cs231n.data_utils import load_CIFAR10
import numpy as np
import matplotlib
matplotlib.use('Agg')
import pylab
import matplotlib.pyplot as plt
import time
from cs231n.classifiers.linear_svm import svm_loss_naive
from cs231n.classifiers.linear_svm import svm_loss_vectorized
from cs231n.classifiers.linear_classifier import LinearSVM
from cs231n.classifiers.linear_classifier import Softmax
from cs231n.gradient_check import grad_check_sparse

def svm_sgd(X_train, y_train,X_val, y_val,X_test, y_test):

    #svm = LinearSVM()
    #tic = time.time()
    #loss_hist = svm.train(X_train, y_train, learning_rate=1e-7, reg=5e-4,num_iters=1500,verbose=True)
    #toc = time.time()
    
    #print 'That took %fs' % (toc-tic)
    #plt.plot(loss_hist)
    #plt.xlabel('Iteration number')
    #plt.ylabel('Loss value')
    #plt.savefig('figures/svm_loss_iteration.png')

    #y_train_pred = svm.predict(X_train)
    #print 'training accuracy: %f' %(np.mean(y_train == y_train_pred),)
    #y_val_pred = svm.predict(X_val)
    #print 'validation accuracy: %f' %(np.mean(y_val == y_val_pred),)

    learning_rates = [1e-7,1e-6,5e-5]
    regs = [5e-4,5e-5,1e-5]
    results = {}
    best_val = -1
    bets_svm = None

    for l in learning_rates:
        for r in regs:
            svm = LinearSVM()
            loss_hist = svm.train(X_train,y_train,learning_rate=l,reg=r,num_iters=500,verbose=True)
            y_train_pred = svm.predict(X_train)
            train_acc = np.mean(y_train == y_train_pred)
            y_val_pred = svm.predict(X_val)
            val_acc = np.mean(y_val == y_val_pred)
            if best_val < val_acc:
                best_val = val_acc
                best_svm = svm
            results[(l,r)] = (train_acc,val_acc)
    
    for lr, reg in sorted(results):
        train_accuracy, val_accuracy = results[(lr, reg)]
        print 'lr %e reg %e train accuracy: %f val accuracy: %f' % (
                lr, reg, train_accuracy, val_accuracy)

    return 
    import math
    x_scatter = [math.log10(x[0]) for x in results]
    y_scatter = [math.log10(x[1]) for x in results]

    # plot training accuracy
    sz = [results[x][0]*1500 for x in results] # default size of markers is 20
    plt.subplot(1,2,1)
    plt.scatter(x_scatter, y_scatter, sz)
    plt.xlabel('log learning rate')
    plt.ylabel('log regularization strength')
    plt.title('CIFAR-10 training accuracy')

    # plot validation accuracy
    sz = [results[x][1]*1500 for x in results] # default size of markers is 20
    plt.subplot(1,2,2)
    plt.scatter(x_scatter, y_scatter, sz)
    plt.xlabel('log learning rate')
    plt.ylabel('log regularization strength')
    plt.title('CIFAR-10 validation accuracy')
    print 'best validation accuracy achieved during cross-validation: %f' % best_val
    plt.savefig('./figures/learn_rate_reg_SVM.png')
    plt.close()

    # Evaluate the best svm on test set
    y_test_pred = best_svm.predict(X_test)
    test_accuracy = np.mean(y_test == y_test_pred)
    print 'linear SVM on raw pixels final test set accuracy: %f' % test_accuracy   

    w = best_svm.W[:,:-1] # strip out the bias
    w = w.reshape(10, 32, 32, 3)
    w_min, w_max = np.min(w), np.max(w)
    classes = ['plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
    for i in xrange(10):
        plt.subplot(2, 5, i + 1)
        
        # Rescale the weights to be between 0 and 255
        wimg = 255.0 * (w[i].squeeze() - w_min) / (w_max - w_min)
        plt.imshow(wimg.astype('uint8'))
        plt.axis('off')
        plt.title(classes[i])
    plt.savefig('./figures/visulize_Wg_SVM.png')

from cs231n.classifiers.softmax import *

def softmax_sgd(X_train,y_train, X_val, y_val,X_test,y_test):
    #W = np.random.randn(10,3073)*0.0001
    #loss, grad = softmax_loss_vectorized(W, X_train,y_train,0.0)
    #print 'loss: %f' % loss
    #print 'sanity check %f' % (-np.log(0.1))
    
    #f = lambda w: softmax_loss_vectorized(w, X_train,y_train,0.0)[0]
    #grad_check_sparse(f,W,grad,10)

    learning_rates = [1e-7,1e-6,5e-5]
    regs = [5e-4,5e-5,1e-5]
    results = {}
    best_val = -1
    bets_soft = None

    for l in learning_rates:
        for r in regs:
            softmax = Softmax()
            loss_hist = softmax.train(X_train,y_train,learning_rate=l,reg=r,num_iters=500,verbose=True)
            y_train_pred = softmax.predict(X_train)
            train_acc = np.mean(y_train == y_train_pred)
            y_val_pred = softmax.predict(X_val)
            val_acc = np.mean(y_val == y_val_pred)
            if best_val < val_acc:
                best_val = val_acc
                best_soft = softmax
            results[(l,r)] = (train_acc,val_acc)
    
    for lr, reg in sorted(results):
        train_accuracy, val_accuracy = results[(lr, reg)]
        print 'lr %e reg %e train accuracy: %f val accuracy: %f' % (
                lr, reg, train_accuracy, val_accuracy)

    
def test2():
    cifar10_dir = 'cs231n/datasets/cifar-10-batches-py'
    X_train, y_train, X_test, y_test = load_CIFAR10(cifar10_dir)

    num_training = 49000
    num_validation = 1000
    mask = range(num_training,num_training+num_validation)
    X_val = X_train[mask]
    y_val = y_train[mask]
    
    mask = range(num_training)
    X_train = X_train[mask]
    y_train = y_train[mask]

    num_test = 1000
    mask = range(num_test)
    X_test = X_test[mask]
    y_test = y_test[mask]

    # print 'Train data shape: ', X_train.shape
    # print 'Train labels shape: ', y_train.shape
    # print 'Validation data shape: ', X_val.shape
    # print 'Validation labels shape: ', y_val.shape
    # print 'Test data shape: ', X_test.shape
    # print 'Test labels shape: ', y_test.shape
    
    # Preprocessing: reshape the image data into rows
    X_train = np.reshape(X_train, (X_train.shape[0], -1))
    X_val = np.reshape(X_val, (X_val.shape[0], -1))
    X_test = np.reshape(X_test, (X_test.shape[0], -1))

    # As a sanity check, print out the shapes of the data
    # print 'Training data shape: ', X_train.shape
    # print 'Validation data shape: ', X_val.shape
    # print 'Test data shape: ', X_test.shape


    mean_image = np.mean(X_train,axis=0)
    #print mean_image[:10]
    #plt.figure(figsize=(4,4))
    #plt.imshow(mean_image.reshape((32,32,3)).astype('uint8'))
    #plt.savefig('./figures/svm_mean.png')
    X_train -= mean_image
    X_val -= mean_image
    X_test -= mean_image

    X_train = np.hstack([X_train,np.ones((X_train.shape[0],1))]).T
    X_val = np.hstack([X_val,np.ones((X_val.shape[0],1))]).T
    X_test = np.hstack([X_test,np.ones((X_test.shape[0],1))]).T


    svm_sgd(X_train,y_train, X_val, y_val,X_test,y_test)
    #softmax_sgd(X_train,y_train, X_val, y_val,X_test,y_test)
    return 
    W = np.random.randn(10,3073)*0.0001
    # loss, grad = svm_loss_naive(W,X_train, y_train,0.00001)
    # print 'loss: %f' %(loss,)

    #loss, grad = svm_loss_naive(W,X_train,y_train,0.0)
    #loss, grad = svm_loss_vectorized(W,X_train,y_train,0.0)

    #f = lambda w: svm_loss_naive(w,X_train, y_train,0.0)[0]
    #grad_check_sparse(f, W, grad, 10)

    tic = time.time()
    loss_naive, grad_naive = svm_loss_naive(W, X_train, y_train, 0.00001)
    toc = time.time()
    print 'Naive loss: %e ,computed in %fs' % (loss_naive,toc - tic)

    tic = time.time()
    loss_vectorized, grad_vector = svm_loss_vectorized(W, X_train, y_train, 0.00001)
    toc = time.time()
    print 'Vectorized loss: %e, computed in %fs' % (loss_vectorized, toc - tic)

    # The losses should match but your vectorized implementation should be much faster.
    print 'difference: %f' % (loss_naive - loss_vectorized)    
    difference = np.linalg.norm(grad_naive-grad_vector,ord='fro')
    print 'difference of grad :%f' % difference

    
test2()
