import tensorflow as tf


class YOLACTLoss(object):

    def __init__(self, loss_weight_cls=1,
                 loss_weight_box=1.5,
                 loss_weight_mask=6.125,
                 neg_pos_ratio=3,
                 max_masks_for_train=100):
        self._loss_weight_cls = loss_weight_cls
        self._loss_weight_box = loss_weight_box
        self._loss_weight_mask = loss_weight_mask
        self._neg_pos_ratio = neg_pos_ratio
        self._max_masks_for_train = max_masks_for_train

    def loss_yolact(self, pred, label):
        """
        :param anchors:
        :param num_pos:
        :param label: labels dict from dataset
        :param pred:
        :return:
        """
        # all prediction component

        # all label component
        cls_targets = label['cls_targets']
        box_targets = label['box_targets']
        num_pos = label['num_positive']
        positiveness = label['positiveness']
        classes = label['classes']
        masks = label['mask_target']

        # _loss_location(pred_offset, gt_offset, positive_indices)

        # calculate the area of pred bounding boxes (anchors, pre_offset) for normalize the cls loss

        # _loss_class(pred_cls, gt_cls, positive_indices, neg_pos_ration)

        pass

    def _loss_location(self, pred_offset, gt_offset, positiveness):
        """
        :param pred_offset: [batch, num_anchor, 4]
        :param gt_offset (box_target): [batch, num_anchor, 4]
        :return:
        """
        positiveness = tf.expand_dims(positiveness, axis=-1)

        # get postive indices
        pos_indices = tf.where(positiveness > 0)

        pred_offset = tf.gather_nd(pred_offset, pos_indices[:, :-1])
        gt_offset = tf.gather_nd(gt_offset, pos_indices[:, :-1])

        # calculate the smoothL1(positive_pred, positive_gt) and return
        smoothl1loss = tf.keras.losses.Huber(delta=0.5)
        loss_loc = tf.reduce_sum(smoothl1loss(gt_offset, pred_offset))
        tf.print("loss_loc:", loss_loc)
        return loss_loc

    def _loss_class(self, pred_cls, gt_cls, num_cls, positiveness, num_pos):
        """

        :param pred_cls: [batch, num_anchor, num_cls]
        :param gt_cls: [batch, num_anchor, 1]
        :param num_cls:
        :param positive_indices:
        :param neg_pos_ratio:
        :return:
        """
        # reshape pred_cls from [batch, num_anchor, num_cls] => [batch * num_anchor, num_cls]
        pred_cls = tf.reshape(-1, num_cls)
        tf.print("pred_cls:", tf.shape(pred_cls))

        # reshape gt_cls from [batch, num_anchor] => [batch * num_anchor, 1]
        gt_cls = tf.expand_dims(gt_cls, axis=-1)
        gt_cls = tf.reshape(-1, 1)
        tf.print("gt_cls:", tf.shape(gt_cls))

        # apply softmax on the pred_cls
        softmax_pred_cls = tf.nn.softmax(pred_cls)

        # -log(softmax class 0)
        loss_minus_log_class0 = tf.expand_dims(-1 * tf.math.log(softmax_pred_cls[:, 0]), axis=-1)

        # reshape positiveness to [batch*num_anchor, 1]
        positiveness = tf.expand_dims(positiveness, axis=-1)
        positiveness = tf.reshape(positiveness, [-1, 1])
        pos_indices = tf.where(positiveness > 0)

        # calculate the needed amount of  negative sample
        num_neg_needed = num_pos * self._neg_pos_ratio

        # eliminate the pos, neutral samples index

        # take the first num_neg_needed idx in sort result and handle the situation if there are not enough neg

        # combine the indices of pos and neg sample, create the label for them

        # calculate Cross entropy loss and return

        pass

    def _loss_mask(self, proto_output, pred_mask_coef, gt_cls, gt_offset, gt_masks, positive_indices,
                   max_masks_for_train):
        """
        loss of linear combination loss
        :return:
        """
        num_batch = tf.shape(proto_output)[0]
        tf.print("Batch_size:", num_batch)
        loss_mask = 0
        # Todo let s see if access by index is available
        for idx in tf.range(num_batch):
            # extract randomly postive sample in pred_mask_coef, gt_cls, gt_offset according to positive_indices
            # calculate sigmoid(pred_mask_coef_positive @ proto_output => [138, 138, num_pos])
            # create [138, 138, num_pos] correspond gt mask
            # iterate the each pair of pred_mask and gt_mask, calculate loss with cropped box
            # loss_mask += BCE(pred_mask, gt_mask)
            pass

        pass